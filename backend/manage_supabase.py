"""连接检查、现有本地投稿迁移。默认只检查，--apply 才实际上传。"""
import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / '.env')

from submission_store import SupabaseStore


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'migrate', 'retry-deletes'])
    parser.add_argument('--apply', action='store_true', help='实际执行云端写入；默认只预览')
    args = parser.parse_args()
    store = SupabaseStore()
    store.check()
    print('Supabase 数据表及两个存储桶连接正常，私有/公开设置正确。')
    if args.command == 'check':
        return
    if args.command == 'retry-deletes':
        # 分批取第一页，删除后继续取，避免翻页跳过记录。
        while True:
            rows = store._table().select('id,kind').eq('deleting', True).limit(100).execute().data
            for row in rows:
                if args.apply:
                    store.delete(row['kind'], row['id'])
                print(f'{row["kind"]} #{row["id"]}: ' + ('已清理' if args.apply else '等待清理'))
            if not args.apply or not rows:
                break
        return
    data_dir = Path(__file__).parent / 'data'
    for kind in ('gallery', 'business_cards'):
        records = json.loads((data_dir / f'{kind}.json').read_text(encoding='utf-8'))
        for record in records:
            result = store.import_local(kind, record, apply=args.apply)
            print(f'{kind} #{record["id"]}: {result}')
    if not args.apply:
        print('预检完成；确认后运行 python manage_supabase.py migrate --apply。')
    else:
        print('迁移完成；本地文件未删除。已迁移的记录在重跑时会跳过。')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # 仅输出异常类型，避免把 SDK 异常中可能含有的密钥/签名链接复制到聊天。
        print(f'操作失败（{type(exc).__name__}）。请检查依赖、项目 URL、服务端密钥和 SQL 初始化。', file=sys.stderr)
        sys.exit(1)
