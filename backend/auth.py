"""管理员认证：密码校验 + 签名令牌。

管理员凭据来自 .env（ADMIN_USERNAME / ADMIN_PASSWORD_HASH），
密码以 pbkdf2 哈希存储，明文不落盘。
"""
import os
import hmac
from functools import wraps

from flask import jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

TOKEN_SALT = 'admin-session'
TOKEN_MAX_AGE = 12 * 60 * 60  # 12 小时


def _secret_key() -> str:
    key = os.getenv('SECRET_KEY')
    if not key:
        raise RuntimeError('缺少 SECRET_KEY，请在 backend/.env 中设置。')
    return key


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(_secret_key(), salt=TOKEN_SALT)


def verify_credentials(username: str, password: str) -> bool:
    """用户名 + 密码是否匹配 .env 中配置的管理员。"""
    expected_user = os.getenv('ADMIN_USERNAME', '')
    password_hash = os.getenv('ADMIN_PASSWORD_HASH', '')
    if not expected_user or not password_hash:
        raise RuntimeError('未配置管理员账号，请在 backend/.env 中设置 '
                           'ADMIN_USERNAME 与 ADMIN_PASSWORD_HASH。')
    # 用户名比较也走常量时间，避免泄漏长度以外的信息
    user_ok = hmac.compare_digest(username or '', expected_user)
    pass_ok = check_password_hash(password_hash, password or '')
    return user_ok and pass_ok


def issue_token(username: str) -> str:
    return _serializer().dumps({'u': username})


def read_token(token: str):
    """令牌有效时返回用户名，否则返回 None。"""
    try:
        data = _serializer().loads(token, max_age=TOKEN_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None
    return data.get('u')


def current_admin():
    """从 Authorization: Bearer <token> 解析当前管理员。"""
    header = request.headers.get('Authorization', '')
    if not header.startswith('Bearer '):
        return None
    return read_token(header[7:].strip())


def admin_required(fn):
    """保护管理接口：无有效令牌返回 401。"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        admin = current_admin()
        if not admin:
            return jsonify({"success": False, "error": "未登录或登录已过期"}), 401
        return fn(*args, **kwargs)
    return wrapper


def hash_password(password: str) -> str:
    """生成可写入 .env 的密码哈希（供 create_admin.py 使用）。"""
    return generate_password_hash(password, method='pbkdf2:sha256:600000')
