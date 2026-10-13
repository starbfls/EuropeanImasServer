from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import secrets
import threading
from datetime import datetime
from pathlib import Path

from auth import admin_required, current_admin, issue_token, verify_credentials
from uploads import (
    MAX_IMAGE_BYTES,
    UPLOAD_ROOT,
    UploadError,
    check_rate_limit,
    delete_upload,
    rollback_rate_limit,
    save_image,
)

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── 数据与上传 ────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / 'data'
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 3 * MAX_IMAGE_BYTES   # 整个请求上限

# 照片墙分类来自 data/gallery_types.json，加一场 live 只要改那个文件，
# 不用动代码。每项形如 {"id": "million14th", "label": "百万现场 14th", "group": "现地"}。


def gallery_types() -> list:
    try:
        return load_data('gallery_types.json')
    except (OSError, ValueError):
        return []


def gallery_type_map() -> dict:
    return {t['id']: t for t in gallery_types() if t.get('id')}

_write_lock = threading.Lock()


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
    """从 data/ 目录读取 JSON 文件并返回列表。"""
    path = DATA_DIR / filename
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_data(filename: str, data: list) -> None:
    """原子写回 data/ 目录下的 JSON 文件。"""
    path = DATA_DIR / filename
    tmp = path.with_suffix('.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(tmp, path)


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
    """用分类表里的最新名字覆盖快照，分类改名后老照片也跟着更新。"""
    t = gallery_type_map().get(photo.get('type'))
    if t:
        return {**photo, 'type_label': t.get('label', photo.get('type'))}
    return {**photo, 'type_label': photo.get('type_label') or photo.get('type')}


@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    data = load_data('gallery.json')
    approved = [p for p in data if p.get("approved")]
    approved.sort(key=lambda p: p.get("submitted_at", ""), reverse=True)
    return jsonify({"success": True, "data": [_with_label(p) for p in approved]})


@app.route('/api/gallery/types', methods=['GET'])
def get_gallery_types():
    """投稿表单与筛选栏共用的分类列表。"""
    return jsonify({"success": True, "data": gallery_types()})


@app.route('/api/gallery', methods=['POST'])
def submit_gallery_photo():
    """访客上传照片，落盘后进入待审核队列。"""
    title = (request.form.get('title') or '').strip()
    photo_type = (request.form.get('type') or '').strip()
    uploader = (request.form.get('uploader') or '').strip()
    photo = request.files.get('photo')

    if not title:
        return jsonify({"success": False, "error": "请填写照片标题"}), 400
    types = gallery_type_map()
    if photo_type not in types:
        return jsonify({"success": False, "error": "请选择一个有效的分类"}), 400
    if not photo:
        return jsonify({"success": False, "error": "请选择要上传的照片"}), 400

    ip = client_ip()
    try:
        check_rate_limit(ip)
    except UploadError as exc:
        return jsonify({"success": False, "error": str(exc)}), 429

    try:
        saved = save_image(photo, 'gallery', 'photo', thumbnail=True)
    except UploadError as exc:
        rollback_rate_limit(ip)
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception('照片上传处理失败')
        rollback_rate_limit(ip)
        return jsonify({"success": False, "error": "图片处理失败，请换一张试试"}), 400

    with _write_lock:
        photos = load_data('gallery.json')
        photos.append({
            "id": max((p["id"] for p in photos), default=0) + 1,
            "title": title[:60],
            "type": photo_type,
            # 存一份当时的名字：万一以后这个分类从列表里删掉，老照片仍有可读的标签
            "type_label": types[photo_type].get('label', photo_type),
            "url": saved["url"],
            "thumbnail": saved["thumbnail"],
            "uploader": uploader[:30] or "匿名制作人",
            "approved": False,
            "submitted_at": datetime.now().isoformat(timespec='seconds'),
        })
        save_data('gallery.json', photos)

    return jsonify({
        "success": True,
        "message": "照片已提交，正在审核中。审核通过后将显示在照片墙上。"
    }), 201


@app.route('/api/business-cards', methods=['GET'])
def get_business_cards():
    data = load_data('business_cards.json')
    approved = [c for c in data if c.get("approved")]
    return jsonify({"success": True, "data": approved})


@app.route('/api/business-cards', methods=['POST'])
def submit_business_card():
    """访客上传名片正反面，落盘后进入待审核队列。"""
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

    saved = []
    try:
        front_url = save_image(front, 'business_cards', 'front')['url']
        saved.append(front_url)
        back_url = save_image(back, 'business_cards', 'back')['url']
        saved.append(back_url)
    except UploadError as exc:
        for url in saved:
            delete_upload(url)
        rollback_rate_limit(ip)
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception('名片上传处理失败')
        for url in saved:
            delete_upload(url)
        rollback_rate_limit(ip)
        return jsonify({"success": False, "error": "图片处理失败，请换一张试试"}), 400

    with _write_lock:
        cards = load_data('business_cards.json')
        cards.append({
            "id": max((c["id"] for c in cards), default=0) + 1,
            "front": front_url,
            "back": back_url,
            "owner": owner[:30],
            "oshi": oshi[:30] or "未填写",
            "approved": False,
            "submitted_at": datetime.now().isoformat(timespec='seconds'),
        })
        save_data('business_cards.json', cards)

    return jsonify({
        "success": True,
        "message": "名片已提交，正在审核中。审核通过后将显示在名片墙上。"
    }), 201


@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    """开发环境下由 Flask 直接提供上传图片；生产环境建议交给 Nginx。"""
    return send_from_directory(UPLOAD_ROOT, filename)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "欧洲偶像大师制作人联盟服务器运行中"})


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
    cards = load_data('business_cards.json')
    if status == 'pending':
        cards = [c for c in cards if not c.get('approved')]
    elif status == 'approved':
        cards = [c for c in cards if c.get('approved')]
    return jsonify({"success": True, "data": cards})


@app.route('/api/admin/business-cards/<int:item_id>/approve', methods=['POST'])
@admin_required
def admin_approve_business_card(item_id):
    with _write_lock:
        cards = load_data('business_cards.json')
        card = next((c for c in cards if c["id"] == item_id), None)
        if not card:
            return jsonify({"success": False, "error": "未找到"}), 404
        card["approved"] = True
        save_data('business_cards.json', cards)
    return jsonify({"success": True, "data": card})


@app.route('/api/admin/business-cards/<int:item_id>', methods=['DELETE'])
@admin_required
def admin_delete_business_card(item_id):
    """驳回或下架：删除记录并清理已上传的图片。"""
    with _write_lock:
        cards = load_data('business_cards.json')
        card = next((c for c in cards if c["id"] == item_id), None)
        if not card:
            return jsonify({"success": False, "error": "未找到"}), 404
        save_data('business_cards.json', [c for c in cards if c["id"] != item_id])
    delete_upload(card.get('front'))
    delete_upload(card.get('back'))
    return jsonify({"success": True, "message": "已删除"})


# ── 管理员：照片墙审核 ────────────────────────────────────────────────────────

@app.route('/api/admin/gallery', methods=['GET'])
@admin_required
def admin_list_gallery():
    """status=pending（默认）/ approved / all。"""
    status = request.args.get('status', 'pending')
    photos = load_data('gallery.json')
    if status == 'pending':
        photos = [p for p in photos if not p.get('approved')]
    elif status == 'approved':
        photos = [p for p in photos if p.get('approved')]
    photos.sort(key=lambda p: p.get('submitted_at', ''), reverse=True)
    return jsonify({"success": True, "data": [_with_label(p) for p in photos]})


@app.route('/api/admin/gallery/<int:item_id>/approve', methods=['POST'])
@admin_required
def admin_approve_gallery(item_id):
    with _write_lock:
        photos = load_data('gallery.json')
        photo = next((p for p in photos if p["id"] == item_id), None)
        if not photo:
            return jsonify({"success": False, "error": "未找到"}), 404
        photo["approved"] = True
        save_data('gallery.json', photos)
    return jsonify({"success": True, "data": photo})


@app.route('/api/admin/gallery/<int:item_id>', methods=['DELETE'])
@admin_required
def admin_delete_gallery(item_id):
    """驳回或下架：删除记录并清理原图与缩略图。"""
    with _write_lock:
        photos = load_data('gallery.json')
        photo = next((p for p in photos if p["id"] == item_id), None)
        if not photo:
            return jsonify({"success": False, "error": "未找到"}), 404
        save_data('gallery.json', [p for p in photos if p["id"] != item_id])
    delete_upload(photo.get('url'))
    if photo.get('thumbnail') != photo.get('url'):
        delete_upload(photo.get('thumbnail'))
    return jsonify({"success": True, "message": "已删除"})


@app.errorhandler(413)
def payload_too_large(_):
    limit = MAX_IMAGE_BYTES // (1024 * 1024)
    return jsonify({"success": False,
                    "error": f"上传内容过大，单张图片请控制在 {limit} MB 以内"}), 413


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    # 默认关闭：开着等于把 Werkzeug 交互式调试器暴露出去，可被远程执行代码
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
