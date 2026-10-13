"""访客上传的图片处理：类型嗅探、落盘、缩略图、容量与频率限制。

免注册上传的三条底线都在这里：
  1. 图片类型按**文件头**判断，不信任用户提供的扩展名；
  2. 单文件大小、上传目录总容量都有上限；
  3. 按 IP 做滑动窗口限流。
"""
import io
import os
import secrets
import threading
import time
from collections import defaultdict, deque
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError
from PIL import features as _pil_features  # noqa: F401  (确保插件已注册)

# 超过这个像素数直接判定为解压炸弹，Pillow 会抛 DecompressionBombError
Image.MAX_IMAGE_PIXELS = 64_000_000

UPLOAD_ROOT = Path(__file__).parent / 'uploads'

# 按文件头识别真实类型 → 落盘用的扩展名。绝不使用上传文件名里的后缀。
MAGIC = (
    (b'\xff\xd8\xff', '.jpg'),
    (b'\x89PNG\r\n\x1a\n', '.png'),
    (b'GIF87a', '.gif'),
    (b'GIF89a', '.gif'),
)

MAX_IMAGE_BYTES = 8 * 1024 * 1024          # 单张原图 8 MB
MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024   # uploads 目录总量 2 GB
MAX_PIXELS = 50_000_000                    # 5000 万像素，超过视为解压炸弹
MAX_STORED_EDGE = 2560                     # 落盘图片最长边，超出等比缩小
THUMB_MAX_EDGE = 640                       # 缩略图最长边

# 重新编码时用的目标格式：输入格式 → (Pillow 格式, 扩展名, 保存参数)
REENCODE = {
    '.jpg':  ('JPEG', '.jpg',  {'quality': 88, 'optimize': True, 'progressive': True}),
    '.png':  ('PNG',  '.png',  {'optimize': True}),
    '.webp': ('WEBP', '.webp', {'quality': 88, 'method': 5}),
    '.gif':  ('GIF',  '.gif',  {'save_all': True, 'optimize': True}),
}

# 限流字典最多保留多少个 IP，防止被伪造来源撑爆内存
MAX_TRACKED_IPS = 20_000

# 每个 IP 在窗口内允许的提交次数（名片与照片共用同一份配额，
# 本质上是给每个 IP 的"磁盘写入预算"）。聚会后一次传几十张是常态，
# 所以给得比较宽；真正的兜底是 MAX_TOTAL_BYTES 和人工审核。
RATE_LIMIT = 30
RATE_WINDOW = 60 * 60

_rate_hits = defaultdict(deque)
_rate_lock = threading.Lock()


class UploadError(ValueError):
    """面向用户的上传失败原因，调用方直接把 message 返回给前端。"""


# ── 频率限制 ──────────────────────────────────────────────────────────────────

def _prune_rate_table(now: float) -> None:
    """清掉窗口外的 IP，避免字典被大量来源撑爆内存。调用方需持锁。"""
    stale = [k for k, v in _rate_hits.items() if not v or now - v[-1] > RATE_WINDOW]
    for k in stale:
        del _rate_hits[k]


def check_rate_limit(ip: str) -> None:
    """滑动窗口限流。注意：计数在进程内存里，多 worker 部署时需要换成共享存储。"""
    now = time.time()
    with _rate_lock:
        if len(_rate_hits) > MAX_TRACKED_IPS:
            _prune_rate_table(now)
        hits = _rate_hits[ip or 'unknown']
        while hits and now - hits[0] > RATE_WINDOW:
            hits.popleft()
        if len(hits) >= RATE_LIMIT:
            wait = int((RATE_WINDOW - (now - hits[0])) / 60) + 1
            raise UploadError(f'上传过于频繁，请 {wait} 分钟后再试')
        hits.append(now)


def rollback_rate_limit(ip: str) -> None:
    """上传因为别的原因失败时，把刚才记的那一次还回去。"""
    with _rate_lock:
        hits = _rate_hits.get(ip or 'unknown')
        if hits:
            hits.pop()


# ── 容量 ──────────────────────────────────────────────────────────────────────

def total_upload_bytes() -> int:
    total = 0
    for path in UPLOAD_ROOT.rglob('*'):
        if path.is_file():
            try:
                total += path.stat().st_size
            except OSError:
                pass
    return total


# ── 保存 ──────────────────────────────────────────────────────────────────────

def _sniff(head: bytes) -> str:
    for magic, ext in MAGIC:
        if head.startswith(magic):
            return ext
    if head[:4] == b'RIFF' and head[8:12] == b'WEBP':
        return '.webp'
    raise UploadError('只支持 JPG / PNG / WEBP / GIF 格式的图片')


def save_image(storage, kind: str, prefix: str, thumbnail: bool = False) -> dict:
    """校验、**重新编码**并保存一张上传的图片。

    kind 是 uploads/ 下的子目录名（business_cards / gallery）。
    返回 {'url': ..., 'thumbnail': ...}，thumbnail=False 时两者相同。

    关键点：落盘的不是用户上传的原始字节，而是 Pillow 重新编码出来的图像。
    这一步同时解决三件事：
      · 清掉 EXIF（GPS 定位、机型、序列号等隐私信息）；
      · 清掉"又是合法图片又是 HTML/脚本"的多态文件和尾部挂载的任意数据；
      · 顺手把超大图缩到 MAX_STORED_EDGE 以内。
    """
    stream = storage.stream
    stream.seek(0, os.SEEK_END)
    size = stream.tell()
    stream.seek(0)
    if size == 0:
        raise UploadError('图片内容为空')
    if size > MAX_IMAGE_BYTES:
        raise UploadError(f'单张图片不能超过 {MAX_IMAGE_BYTES // (1024 * 1024)} MB')

    # 1) 文件头决定类型，绝不相信上传文件名里的后缀
    head = stream.read(16)
    stream.seek(0)
    ext = _sniff(head)
    fmt, out_ext, save_kw = REENCODE[ext]

    # 2) 先只读尺寸（不解码像素），挡掉解压炸弹
    try:
        probe = Image.open(stream)
        w, h = probe.size
        n_frames = getattr(probe, 'n_frames', 1)
    except Image.DecompressionBombError:
        raise UploadError('图片分辨率过高，疑似解压炸弹，请压缩后再上传')
    except Exception:
        raise UploadError('图片已损坏或不是有效的图片文件')
    finally:
        stream.seek(0)

    if w <= 0 or h <= 0:
        raise UploadError('图片尺寸异常')
    if w * h > MAX_PIXELS:
        raise UploadError(
            f'图片分辨率过高（{w}×{h}），请压缩到 {MAX_PIXELS // 1_000_000} 百万像素以内'
        )

    if total_upload_bytes() + size > MAX_TOTAL_BYTES:
        raise UploadError('服务器图片存储空间已满，请联系管理员')

    # 3) 真正解码并重新编码
    try:
        im = Image.open(stream)
        animated = fmt == 'GIF' and n_frames > 1
        if not animated:
            im = ImageOps.exif_transpose(im)          # 按 EXIF 方向摆正，再丢掉 EXIF
            im.thumbnail((MAX_STORED_EDGE, MAX_STORED_EDGE), Image.LANCZOS)
            if fmt == 'JPEG':
                im = im.convert('RGB')                 # JPEG 不支持透明通道
            elif im.mode == 'P' and fmt in ('PNG', 'WEBP'):
                im = im.convert('RGBA')
        else:
            save_kw = dict(save_kw)                    # 动图保持原样，只做重编码
    except Image.DecompressionBombError:
        raise UploadError('图片分辨率过高，疑似解压炸弹')
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError):
        raise UploadError('图片已损坏或不是有效的图片文件')

    target_dir = UPLOAD_ROOT / kind
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = f'{prefix}_{secrets.token_hex(8)}'
    name = stem + out_ext
    dest = target_dir / name

    try:
        # 先编码到内存，确认能写成功再落盘，避免留下半截文件
        buf = io.BytesIO()
        im.save(buf, fmt, **save_kw)
        data = buf.getvalue()
        if len(data) > MAX_IMAGE_BYTES * 2:
            raise UploadError('图片处理后体积过大')
        dest.write_bytes(data)
    except UploadError:
        raise
    except Exception:
        dest.unlink(missing_ok=True)
        raise UploadError('图片处理失败，请换一张试试')
    finally:
        try:
            im.close()
        except Exception:
            pass

    url = f'/uploads/{kind}/{name}'
    if not thumbnail:
        return {'url': url, 'thumbnail': url}

    thumb_name = f'{stem}_thumb.webp'
    try:
        with Image.open(dest) as t:
            t = t.convert('RGB')
            t.thumbnail((THUMB_MAX_EDGE, THUMB_MAX_EDGE), Image.LANCZOS)
            t.save(target_dir / thumb_name, 'WEBP', quality=82, method=5)
        thumb_url = f'/uploads/{kind}/{thumb_name}'
    except Exception:
        thumb_url = url          # 缩略图失败不影响主流程，退回用原图

    return {'url': url, 'thumbnail': thumb_url}


def delete_upload(url: str) -> None:
    """删除本站上传的图片；外链忽略。"""
    if not url or not url.startswith('/uploads/'):
        return
    rel = url[len('/uploads/'):]
    target = (UPLOAD_ROOT / rel).resolve()
    try:
        # 防目录穿越：只删 uploads 目录内的文件
        target.relative_to(UPLOAD_ROOT.resolve())
    except ValueError:
        return
    try:
        target.unlink(missing_ok=True)
    except OSError:
        pass
