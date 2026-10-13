"""创建 / 重置管理员账号。

用法：
    python create_admin.py                      # 用户名 admin，随机生成密码
    python create_admin.py --username alice     # 指定用户名，随机生成密码
    python create_admin.py --password 'xxx'     # 指定密码

脚本会把用户名与密码哈希写入 backend/.env（明文密码只在终端显示一次），
并在缺少 SECRET_KEY 时自动生成一个。
"""
import argparse
import secrets
import string
from pathlib import Path

from auth import hash_password

ENV_PATH = Path(__file__).parent / '.env'


def read_env() -> dict:
    if not ENV_PATH.exists():
        return {}
    env = {}
    for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        env[key.strip()] = value.strip()
    return env


def write_env(env: dict) -> None:
    lines = [key + '=' + value for key, value in env.items()]
    ENV_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def random_password(length: int = 20) -> str:
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*-_=+'
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def main() -> None:
    parser = argparse.ArgumentParser(description='创建或重置管理员账号')
    parser.add_argument('--username', default='admin', help='管理员用户名（默认 admin）')
    parser.add_argument('--password', default=None, help='管理员密码（省略则随机生成）')
    args = parser.parse_args()

    password = args.password or random_password()

    env = read_env()
    if not env.get('SECRET_KEY'):
        env['SECRET_KEY'] = secrets.token_urlsafe(48)
        print('已生成新的 SECRET_KEY（更换它会使所有已登录的管理员令牌失效）。')
    env['ADMIN_USERNAME'] = args.username
    env['ADMIN_PASSWORD_HASH'] = hash_password(password)
    write_env(env)

    print('')
    print('管理员账号已写入 ' + str(ENV_PATH))
    print('  用户名：' + args.username)
    print('  密  码：' + password)
    print('')
    print('密码只显示这一次，请立刻保存。重启后端后即可在 /admin/login 登录。')


if __name__ == '__main__':
    main()
