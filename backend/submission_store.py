"""照片/名片记录与文件存储。云端只持久保存对象路径，不保存临时签名 URL。"""
import json
import logging
import os
import threading
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from uploads import IMAGE_CONTENT_TYPES, UPLOAD_ROOT, UploadError, delete_upload, prepare_image, save_image

log = logging.getLogger(__name__)
KINDS = {'gallery': ('url', 'thumbnail'), 'business_cards': ('front', 'back')}


class StoreError(RuntimeError):
    pass


def load_supabase_sdk():
    """检查实际 SDK，避免把同名 SQL 目录误认成已安装的依赖。"""
    try:
        from supabase import ClientOptions, create_client
    except ImportError as exc:
        raise StoreError(
            '当前 Python 环境未安装完整的 Supabase SDK。'
            '请在 backend 目录执行 '
            r'.\.venv\Scripts\python.exe -m pip install -r requirements.txt，'
            '然后使用 '
            r'.\.venv\Scripts\python.exe app.py 启动后端。'
        ) from exc
    return ClientOptions, create_client


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


class LocalStore:
    """保留原有 JSON 模式，供未接入云端的本地开发使用。"""
    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir or Path(__file__).parent / 'data')
        self.lock = threading.RLock()

    def _read(self, kind):
        return json.loads((self.data_dir / f'{kind}.json').read_text(encoding='utf-8'))

    def _write(self, kind, rows):
        path = self.data_dir / f'{kind}.json'
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(path)

    def list(self, kind, status='approved'):
        rows = self._read(kind)
        if status != 'all':
            rows = [r for r in rows if bool(r.get('approved')) == (status == 'approved')]
        return sorted(rows, key=lambda r: r.get('submitted_at', ''), reverse=True)

    def create(self, kind, payload, images):
        paths = {}
        try:
            for field, image in images.items():
                saved = save_image(image, kind, field, thumbnail=kind == 'gallery')
                paths[field] = saved['url']
                if kind == 'gallery':
                    paths['thumbnail'] = saved['thumbnail']
            with self.lock:
                rows = self._read(kind)
                row = dict(payload, **paths, id=max((r['id'] for r in rows), default=0) + 1,
                           approved=False, submitted_at=utc_now())
                rows.append(row)
                self._write(kind, rows)
            return row
        except Exception:
            for path in set(paths.values()):
                delete_upload(path)
            raise

    def approve(self, kind, item_id):
        with self.lock:
            rows = self._read(kind)
            row = next((r for r in rows if r['id'] == item_id), None)
            if row:
                row['approved'] = True
                self._write(kind, rows)
            return row

    def delete(self, kind, item_id):
        with self.lock:
            rows = self._read(kind)
            row = next((r for r in rows if r['id'] == item_id), None)
            if not row:
                return False
            self._write(kind, [r for r in rows if r['id'] != item_id])
        for path in {row.get(field) for field in KINDS[kind]}:
            delete_upload(path)
        return True


class SupabaseStore:
    def __init__(self, client=None):
        self.pending_bucket = os.getenv('SUPABASE_PENDING_BUCKET', 'imas-pending')
        self.public_bucket = os.getenv('SUPABASE_PUBLIC_BUCKET', 'imas-public')
        if self.pending_bucket == self.public_bucket:
            raise StoreError('待审核桶和公开桶不能相同')
        self.preview_seconds = 900
        self.lock = threading.RLock()
        if client is None:
            url = os.getenv('SUPABASE_URL', '').strip()
            key = os.getenv('SUPABASE_SECRET_KEY', '').strip() or os.getenv('SUPABASE_SERVICE_ROLE_KEY', '').strip()
            if not url or not key:
                raise StoreError('缺少 SUPABASE_URL / SUPABASE_SECRET_KEY，请按 docs/SUPABASE_SETUP.md 配置')
            ClientOptions, create_client = load_supabase_sdk()
            client = create_client(url, key, options=ClientOptions(
                persist_session=False, auto_refresh_token=False,
                postgrest_client_timeout=30, storage_client_timeout=20,
            ))
        self.client = client

    def _table(self):
        return self.client.table('submissions')

    def _bucket(self, approved=False):
        return self.client.storage.from_(self.public_bucket if approved else self.pending_bucket)

    def check(self):
        """只读连接检查，同时检查桶的公开/私有设置。"""
        self._table().select('id,kind,payload,files,size_bytes,approved,deleting,legacy_key,submitted_at').limit(1).execute()
        for name, public in [(self.pending_bucket, False), (self.public_bucket, True)]:
            bucket = self.client.storage.get_bucket(name)
            actual = bucket.get('public') if isinstance(bucket, dict) else bucket.public
            if actual != public:
                raise StoreError(f'存储桶 {name} 的公开设置不正确')

    def _find(self, kind, item_id):
        rows = self._table().select('*').eq('kind', kind).eq('id', item_id).execute().data
        return rows[0] if rows else None

    def _serialize(self, row, admin=False):
        if not row['approved'] and not admin:
            raise StoreError('不能向公开接口返回待审核投稿')
        result = dict(row['payload'], id=row['id'], approved=row['approved'], submitted_at=row['submitted_at'])
        bucket = self._bucket(row['approved'])
        urls = {}
        for field, path in row['files'].items():
            if path not in urls:
                if row['approved']:
                    urls[path] = bucket.get_public_url(path)
                else:
                    signed = bucket.create_signed_url(path, self.preview_seconds)
                    urls[path] = signed['signedURL']
            result[field] = urls[path]
        if not row['approved']:
            result['preview_expires_in'] = self.preview_seconds
        return result

    def list(self, kind, status='approved'):
        result, offset = [], 0
        # PostgREST 默认有返回行数上限，显式分页，避免投稿多后静默遗漏。
        while True:
            query = self._table().select('*').eq('kind', kind).eq('deleting', False)
            if status != 'all':
                query = query.eq('approved', status == 'approved')
            rows = query.order('submitted_at', desc=True).order('id', desc=True).range(offset, offset + 99).execute().data
            result.extend(self._serialize(r, admin=status != 'approved') for r in rows)
            if len(rows) < 100:
                return result
            offset += 100

    def _remove(self, paths, approved=False, quiet=False):
        if not paths:
            return
        try:
            self._bucket(approved).remove(sorted(set(paths)))
        except Exception:
            if not quiet:
                raise
            log.warning('云端图片清理未完成，请检查 Storage 中的残留对象', exc_info=True)

    def _insert(self, kind, payload, prepared, approved=False, legacy_key=None, submitted_at=None):
        files = {field: asset['path'] for field, asset in prepared.items()}
        unique = {asset['path']: asset for asset in prepared.values()}
        uploaded = []
        try:
            for path, asset in unique.items():
                # 先登记待清理路径；网络超时也可能已经在服务端写入成功。
                uploaded.append(path)
                self._bucket(approved).upload(path, asset['data'], file_options={
                    'content-type': asset['content_type'], 'cache-control': '60', 'upsert': 'false',
                })
            value = {'kind': kind, 'payload': payload, 'files': files,
                     'size_bytes': sum(len(a['data']) for a in unique.values()), 'approved': approved}
            if legacy_key:
                value['legacy_key'] = legacy_key
            if submitted_at:
                value['submitted_at'] = submitted_at
            rows = self._table().insert(value).execute().data
            if not rows:
                raise StoreError('数据库未返回新投稿')
            return rows[0]
        except Exception as exc:
            # insert 超时可能已提交。通过唯一对象路径查询，避免删除成功记录的图片。
            try:
                rows = self._table().select('id').contains('files', files).limit(1).execute().data
                if rows:
                    return self._find(kind, rows[0]['id'])
            except Exception:
                log.warning('无法确认投稿是否已经写入；保留对象供人工核对')
                raise
            self._remove(uploaded, approved, quiet=True)
            if 'media_storage_quota_exceeded' in str(exc):
                raise UploadError('云端图片存储配额已满，请联系管理员') from exc
            raise

    def create(self, kind, payload, images):
        prepared = {}
        # 所有图片全部校验完成后再开始云端写入。
        for field, image in images.items():
            assets = prepare_image(image, kind, field, thumbnail=kind == 'gallery')
            prepared[field] = assets['image']
            if kind == 'gallery':
                prepared['thumbnail'] = assets['thumbnail']
        row = self._insert(kind, payload, prepared)
        return {'id': row['id']}

    def approve(self, kind, item_id):
        with self.lock:
            row = self._find(kind, item_id)
            if not row or row['deleting']:
                return None
            if row['approved']:
                return self._serialize(row, admin=True)
            paths = sorted(set(row['files'].values()))
            uploaded = []
            try:
                for path in paths:
                    content_type = IMAGE_CONTENT_TYPES.get(Path(path).suffix.lower())
                    if not content_type:
                        raise StoreError('投稿包含不支持的图片格式，请联系管理员检查存储记录')
                    data = self._bucket().download(path)
                    uploaded.append(path)
                    self._bucket(True).upload(path, data, file_options={
                        'content-type': content_type,
                        'cache-control': '60', 'upsert': 'true',
                    })
                rows = self._table().update({'approved': True}).eq('id', item_id).eq('kind', kind).eq('deleting', False).execute().data
                if not rows:
                    raise StoreError('投稿状态已改变，请刷新后重试')
            except Exception:
                # 更新响应可能丢失；只有确认仍未批准时才撤销公开副本。
                current = self._find(kind, item_id)
                if not current or not current['approved']:
                    self._remove(uploaded, True, quiet=True)
                    raise
                rows = [current]
            self._remove(paths, quiet=True)
            return self._serialize(rows[0], admin=True)

    def delete(self, kind, item_id):
        with self.lock:
            row = self._find(kind, item_id)
            if not row:
                return False
            # 删除中记录立即从列表隐藏；清理失败保留记录，重试 DELETE 即可继续。
            self._table().update({'deleting': True}).eq('id', item_id).eq('kind', kind).execute()
            paths = list(row['files'].values())
            self._remove(paths, True)
            self._remove(paths)
            self._table().delete().eq('id', item_id).eq('kind', kind).execute()
            return True

    def import_local(self, kind, record, upload_root=UPLOAD_ROOT, apply=False):
        """迁移已有图片，不删除本地文件；legacy_key 使重跑可跳过已导入记录。"""
        legacy_key = f'local:{kind}:{record["id"]}'
        existing = self._table().select('id').eq('legacy_key', legacy_key).limit(1).execute().data
        if existing:
            return 'skipped'
        prepared, root = {}, Path(upload_root).resolve()
        for field in KINDS[kind]:
            url = record.get(field) or record.get('url')
            if not url or not url.startswith('/uploads/'):
                raise StoreError(f'{kind} #{record["id"]}: {field} 不是本地上传路径')
            path = (root / url.removeprefix('/uploads/')).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                raise StoreError(f'{kind} #{record["id"]}: 本地图片缺失或路径无效')
            # 与新投稿相同的校验、缩放和隐私信息清理。
            from werkzeug.datastructures import FileStorage
            with path.open('rb') as stream:
                assets = prepare_image(FileStorage(stream=stream, filename=path.name), kind, field)
                prepared[field] = assets['image']
        if apply:
            payload = {k: v for k, v in record.items() if k not in {*KINDS[kind], 'id', 'approved', 'submitted_at'}}
            self._insert(kind, payload, prepared, approved=bool(record.get('approved')),
                         legacy_key=legacy_key, submitted_at=record.get('submitted_at'))
        return 'imported' if apply else 'ready'


@lru_cache(maxsize=1)
def get_store():
    mode = os.getenv('STORAGE_BACKEND', 'local').strip().lower()
    if mode == 'supabase':
        return SupabaseStore()
    if mode == 'local':
        return LocalStore()
    raise StoreError('STORAGE_BACKEND 只能为 local 或 supabase')
