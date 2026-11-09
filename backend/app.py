from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import sys
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')

from auth import admin_required, current_admin, issue_token, verify_credentials
from submission_store import StoreError, get_store, load_supabase_sdk
from uploads import (
    MAX_IMAGE_BYTES,
    UPLOAD_ROOT,
    UploadError,
    check_rate_limit,
    rollback_rate_limit,
)

app = Flask(__name__)
CORS(app)

# ── 数据与上传 ────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / 'data' / 'content'
if os.getenv('STORAGE_BACKEND', 'local') == 'local':
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 3 * MAX_IMAGE_BYTES   # 整个请求上限

# 照片墙分类来自 data/content/gallery_types.json，加一场 live 只要改那个文件，
# 不用动代码。每项形如 {"id": "million14th", "label": "百万现场 14th", "group": "现地"}。


def gallery_types() -> list:
    try:
        return load_data('gallery_types.json')
    except (OSError, ValueError):
        return []


def gallery_type_map() -> dict:
    return {t['id']: t for t in gallery_types() if t.get('id')}


# 只有确实部署在反向代理后面时才把 X-Forwarded-For 当真。
# 默认关闭：否则任何人都能伪造这个头，给自己换一个“新 IP”，限流形同虚设。
TRUST_PROXY = os.getenv('TRUST_PROXY', 'false').lower() == 'true'


def client_ip() -> str:
    """取真实来源 IP。

    TRUST_PROXY=true 时取 X-Forwarded-For 最右侧那一跳（由我们自己的反代写入，
    客户端伪造的部分都在左边，覆盖不掉）；否则一律用 TCP 对端地址。
    """
    if TRUST_PROXY:
        forwarded = request.headers.get('X-Forwarded-For', '')
        if forwarded:
            return forwarded.split(',')[-1].strip()
    return request.remote_addr or 'unknown'


@app.after_request
def security_headers(resp):
    """全站安全头。

    上传目录额外套一层 CSP 沙箱：即使有人传上来"既是合法图片又是 HTML"的
    多态文件，浏览器也不会把它当页面执行。
    """
    resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
    resp.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
    resp.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
    if request.path.startswith('/uploads/'):
        resp.headers['Content-Security-Policy'] = (
            "default-src 'none'; img-src 'self'; sandbox"
        )
        resp.headers['Cross-Origin-Resource-Policy'] = 'same-site'
    return resp


def load_data(filename: str) -> list:
    """读取由 Git 管理的活动内容与分类，不涉及用户投稿。"""
    path = DATA_DIR / filename
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ── 公开 API ──────────────────────────────────────────────────────────────────

@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    data = load_data('announcements.json')
    return jsonify({"success": True, "data": data})


@app.route('/api/announcements/<int:item_id>', methods=['GET'])
def get_announcement_detail(item_id):
    data = load_data('announcements.json')
    item = next((a for a in data if a["id"] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": "未找到"}), 404
    return jsonify({"success": True, "data": item})


@app.route('/api/imas-events', methods=['GET'])
def get_imas_events():
    """偶像大师官方演唱会 / 活动日历，按开始日期升序。"""
    data = load_data('imas_events.json')
    data.sort(key=lambda e: e['date_start'])
    return jsonify({"success": True, "data": data})


def _with_label(photo: dict) -> dict:
    """统一新多标签与旧单标签记录，标签名称始终取分类表的最新值。"""
    raw_types = photo.get('types')
    if not isinstance(raw_types, list) or not raw_types:
        raw_types = [photo.get('type')]
    tag_ids = list(dict.fromkeys(tag.strip() for tag in raw_types if isinstance(tag, str) and tag.strip()))
    type_map = gallery_type_map()
    labels = [type_map.get(tag, {}).get('label') or
              (photo.get('type_label') if len(tag_ids) == 1 else None) or tag
              for tag in tag_ids]
    return {**photo, 'type': tag_ids[0] if tag_ids else '', 'types': tag_ids,
            'type_labels': labels, 'type_label': ' · '.join(labels)}


@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    try:
        rows = get_store().list('gallery')
        return jsonify({"success": True, "data": [_with_label(p) for p in rows]})
    except Exception:
        return storage_error()


@app.route('/api/gallery/types', methods=['GET'])
def get_gallery_types():
    """投稿表单与筛选栏共用的分类列表。"""
    return jsonify({"success": True, "data": gallery_types()})


@app.route('/api/gallery', methods=['POST'])
def submit_gallery_photo():
    """访客上传照片；云端模式下先保存到私有桶，审核前不公开。"""
    title = (request.form.get('title') or '').strip()
    # Repeated multipart fields carry the selected tags; accept the old single field too.
    raw_types = request.form.getlist('types') if 'types' in request.form else [request.form.get('type', '')]
    photo_types = list(dict.fromkeys(tag.strip() for tag in raw_types))
    uploader = (request.form.get('uploader') or '').strip()
    photo = request.files.get('photo')

    if not title:
        return jsonify({"success": False, "error": "请填写照片标题"}), 400
    types = gallery_type_map()
    if not photo_types or any(tag not in types for tag in photo_types):
        return jsonify({"success": False, "error": "请选择至少一个有效的照片标签；如标签已更新，请刷新后重新选择。"}), 400
    if not photo:
        return jsonify({"success": False, "error": "请选择要上传的照片"}), 400

    ip = client_ip()
    try:
        check_rate_limit(ip)
    except UploadError as exc:
        return jsonify({"success": False, "error": str(exc)}), 429

    try:
        get_store().create('gallery', {
            'title': title[:60], 'type': photo_types[0], 'types': photo_types,
            'type_label': ' · '.join(types[tag].get('label', tag) for tag in photo_types),
            'uploader': uploader[:30] or '匿名制作人',
        }, {'url': photo})
    except UploadError as exc:
        rollback_rate_limit(ip)
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        rollback_rate_limit(ip)
        return storage_error()

    return jsonify({
        "success": True,
        "message": "照片已提交，正在审核中。审核通过后将显示在照片墙上。"
    }), 201


@app.route('/api/business-cards', methods=['GET'])
def get_business_cards():
    try:
        return jsonify({"success": True, "data": get_store().list('business_cards')})
    except Exception:
        return storage_error()


@app.route('/api/business-cards', methods=['POST'])
def submit_business_card():
    """访客上传名片正反面，保存后进入待审核队列。"""
    owner = (request.form.get('owner') or '').strip()
    oshi = (request.form.get('oshi') or '').strip()
    front = request.files.get('front')
    back = request.files.get('back')

    if not owner:
        return jsonify({"success": False, "error": "请填写制作人称号"}), 400
    if not front or not back:
        return jsonify({"success": False, "error": "请同时上传名片正面与背面"}), 400

    ip = client_ip()
    try:
        check_rate_limit(ip)
    except UploadError as exc:
        return jsonify({"success": False, "error": str(exc)}), 429

    try:
        get_store().create('business_cards', {'owner': owner[:30], 'oshi': oshi[:30] or '未填写'},
                           {'front': front, 'back': back})
    except UploadError as exc:
        rollback_rate_limit(ip)
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        rollback_rate_limit(ip)
        return storage_error()

    return jsonify({
        "success": True,
        "message": "名片已提交，正在审核中。审核通过后将显示在名片墙上。"
    }), 201


@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    """仅兼容本地开发图片，云端模式不暴露遗留上传目录。"""
    if os.getenv('STORAGE_BACKEND', 'local').strip().lower() != 'local':
        return jsonify({'success': False, 'error': '未找到'}), 404
    return send_from_directory(UPLOAD_ROOT, filename)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "欧洲偶像大师制作人联盟服务器运行中"})


def storage_error():
    # 详细异常仅留在服务端；不向浏览器泄漏云端响应、签名 URL 或配置。
    app.logger.exception('投稿存储服务操作失败')
    return jsonify({'success': False, 'error': '投稿存储服务暂时不可用，请稍后重试；管理员可检查后端日志。'}), 503


# ── 管理员 API ────────────────────────────────────────────────────────────────

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    body = request.get_json(silent=True) or {}
    username = body.get('username', '')
    password = body.get('password', '')
    if not verify_credentials(username, password):
        return jsonify({"success": False, "error": "用户名或密码错误"}), 401
    return jsonify({
        "success": True,
        "data": {"token": issue_token(username), "username": username},
    })


@app.route('/api/admin/me', methods=['GET'])
@admin_required
def admin_me():
    """前端用来校验本地保存的令牌是否仍然有效。"""
    return jsonify({"success": True, "data": {"username": current_admin()}})


@app.route('/api/admin/business-cards', methods=['GET'])
@admin_required
def admin_list_business_cards():
    """status=pending（默认）/ approved / all。"""
    status = request.args.get('status', 'pending')
    if status not in ('pending', 'approved', 'all'):
        return jsonify({'success': False, 'error': '无效的审核状态'}), 400
    try:
        return jsonify({"success": True, "data": get_store().list('business_cards', status)})
    except Exception:
        return storage_error()


@app.route('/api/admin/business-cards/<int:item_id>/approve', methods=['POST'])
@admin_required
def admin_approve_business_card(item_id):
    try:
        card = get_store().approve('business_cards', item_id)
        if not card:
            return jsonify({"success": False, "error": "未找到"}), 404
        return jsonify({"success": True, "data": card})
    except Exception:
        return storage_error()


@app.route('/api/admin/business-cards/<int:item_id>', methods=['DELETE'])
@admin_required
def admin_delete_business_card(item_id):
    """驳回或下架：删除记录并清理已上传的图片。"""
    try:
        if not get_store().delete('business_cards', item_id):
            return jsonify({"success": False, "error": "未找到"}), 404
        return jsonify({"success": True, "message": "已删除"})
    except Exception:
        return storage_error()


# ── 管理员：照片墙审核 ────────────────────────────────────────────────────────

@app.route('/api/admin/gallery', methods=['GET'])
@admin_required
def admin_list_gallery():
    """status=pending（默认）/ approved / all。"""
    status = request.args.get('status', 'pending')
    if status not in ('pending', 'approved', 'all'):
        return jsonify({'success': False, 'error': '无效的审核状态'}), 400
    try:
        photos = get_store().list('gallery', status)
        return jsonify({"success": True, "data": [_with_label(p) for p in photos]})
    except Exception:
        return storage_error()


@app.route('/api/admin/gallery/<int:item_id>/approve', methods=['POST'])
@admin_required
def admin_approve_gallery(item_id):
    try:
        photo = get_store().approve('gallery', item_id)
        if not photo:
            return jsonify({"success": False, "error": "未找到"}), 404
        return jsonify({"success": True, "data": _with_label(photo)})
    except Exception:
        return storage_error()


@app.route('/api/admin/gallery/<int:item_id>', methods=['DELETE'])
@admin_required
def admin_delete_gallery(item_id):
    """驳回或下架：删除记录并清理原图与缩略图。"""
    try:
        if not get_store().delete('gallery', item_id):
            return jsonify({"success": False, "error": "未找到"}), 404
        return jsonify({"success": True, "message": "已删除"})
    except Exception:
        return storage_error()


@app.errorhandler(413)
def payload_too_large(_):
    limit = MAX_IMAGE_BYTES // (1024 * 1024)
    return jsonify({"success": False,
                    "error": f"上传内容过大，单张图片请控制在 {limit} MB 以内"}), 413


FRONTEND_DIST = Path(__file__).parent.parent / 'frontend' / 'dist'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def frontend_page(path):
    """生产环境同域提供 Vue 页面；未知 API 不能回退成 HTML。"""
    if path == 'api' or path.startswith(('api/', 'uploads/')):
        return jsonify({'success': False, 'error': '未找到'}), 404
    root = FRONTEND_DIST.resolve()
    target = (root / path).resolve()
    if not target.is_relative_to(root):
        return jsonify({'success': False, 'error': '未找到'}), 404
    if target.is_file():
        return send_from_directory(root, path)
    # 缺失的 JS/CSS/图片不能伪装成成功返回的 index.html。
    if path.startswith('assets/') or Path(path).suffix:
        return jsonify({'success': False, 'error': '未找到'}), 404
    if not (root / 'index.html').is_file():
        return jsonify({'success': False, 'error': '前端尚未构建，请执行 npm run build 或使用 Vite 开发服务器。'}), 503
    response = send_from_directory(root, 'index.html')
    response.headers['Cache-Control'] = 'no-cache'
    return response


if __name__ == '__main__':
    if os.getenv('STORAGE_BACKEND', 'local') == 'supabase':
        try:
            load_supabase_sdk()
        except StoreError as exc:
            print(f'后端启动失败：{exc}', file=sys.stderr)
            sys.exit(1)
    port = int(os.getenv('PORT', 5000))
    # 默认关闭：开着等于把 Werkzeug 交互式调试器暴露出去，可被远程执行代码
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
