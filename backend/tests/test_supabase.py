"""使用真实 Supabase SDK + HTTP 模拟器验证协议和完整投稿流程，无需云端密钥。"""
import copy
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from PIL import Image
from supabase import ClientOptions, create_client
from werkzeug.datastructures import FileStorage

from submission_store import LocalStore, StoreError, SupabaseStore, get_store
from uploads import UploadError, prepare_image


def picture(fmt='PNG', **options):
    output = io.BytesIO()
    Image.new('RGB', (120, 80), 'blue').save(output, fmt, **options)
    output.seek(0)
    return output


def upload():
    return FileStorage(stream=picture(), filename='untrusted-name.html')


class CloudHTTP:
    """内存模拟 PostgREST / Storage 的 HTTP 边界，业务代码仍运行官方 SDK。"""
    def __init__(self):
        self.rows = []
        self.objects = {'imas-pending': {}, 'imas-public': {}}
        self.calls = []
        self.failures = {}
        self.lose_insert_response = False
        self.quota = False
        self.client = httpx.Client(transport=httpx.MockTransport(self.handle))
        self.sdk = create_client('https://example.supabase.co', 'sb_secret_test_only',
                                 options=ClientOptions(httpx_client=self.client))

    def error_once(self, method, path):
        self.failures[(method, path)] = 1

    def handle(self, req):
        method, path = req.method, req.url.path
        self.calls.append((method, path))
        if self.failures.get((method, path), 0):
            self.failures[(method, path)] -= 1
            return httpx.Response(500, json={'code': 'XX000', 'message': 'simulated outage',
                                             'statusCode': '500', 'error': 'Unavailable'})
        if path == '/rest/v1/submissions':
            rows = self.rows
            for field, condition in req.url.params.multi_items():
                if condition.startswith('eq.'):
                    expected = condition[3:]
                    rows = [r for r in rows if str(r.get(field)).lower() == expected.lower()]
                elif condition.startswith('cs.'):
                    expected = json.loads(condition[3:])
                    rows = [r for r in rows if all(r[field].get(k) == v for k, v in expected.items())]
            if method == 'POST':
                if self.quota:
                    return httpx.Response(400, json={'code': 'P0001', 'message': 'media_storage_quota_exceeded'})
                row = json.loads(req.content)
                row.update(id=max((r['id'] for r in self.rows), default=0) + 1,
                           deleting=False, submitted_at=row.get('submitted_at', '2026-10-17T00:00:00+00:00'))
                self.rows.append(row)
                if self.lose_insert_response:
                    self.lose_insert_response = False
                    raise httpx.ReadError('response lost after commit', request=req)
                return httpx.Response(201, json=[copy.deepcopy(row)])
            if method == 'PATCH':
                value = json.loads(req.content)
                for row in rows:
                    row.update(value)
                return httpx.Response(200, json=copy.deepcopy(rows))
            if method == 'DELETE':
                self.rows = [r for r in self.rows if r not in rows]
                return httpx.Response(200, json=copy.deepcopy(rows))
            rows = sorted(rows, key=lambda r: r['id'], reverse=True)
            offset, limit = int(req.url.params.get('offset', 0)), int(req.url.params.get('limit', 1000))
            return httpx.Response(200, json=copy.deepcopy(rows[offset:offset + limit]))
        if path.startswith('/storage/v1/bucket/'):
            bucket = path.rsplit('/', 1)[1]
            return httpx.Response(200, json={'id': bucket, 'name': bucket, 'public': bucket == 'imas-public',
                                             'created_at': '2026-10-17T00:00:00Z', 'updated_at': '2026-10-17T00:00:00Z',
                                             'owner': '', 'file_size_limit': 16777216, 'allowed_mime_types': None})
        if path.startswith('/storage/v1/object/sign/'):
            resource = path.removeprefix('/storage/v1/object/sign/')
            return httpx.Response(200, json={'signedURL': '/object/sign/' + resource + '?token=test'})
        if path.startswith('/storage/v1/object/'):
            resource = path.removeprefix('/storage/v1/object/').removeprefix('authenticated/')
            bucket, _, key = resource.partition('/')
            if method == 'DELETE':
                for name in json.loads(req.content)['prefixes']:
                    self.objects[bucket].pop(name, None)
                return httpx.Response(200, json=[])
            if method in ('POST', 'PUT'):
                self.objects[bucket][key] = req.content
                return httpx.Response(200, json={'Key': bucket + '/' + key, 'Id': '00000000-0000-0000-0000-000000000001'})
            return httpx.Response(200, content=self.objects[bucket][key])
        raise AssertionError(f'Unexpected HTTP request: {method} {path}')


class SupabaseFlowTests(unittest.TestCase):
    def setUp(self):
        self.cloud = CloudHTTP()
        self.store = SupabaseStore(self.cloud.sdk)
        self.addCleanup(self.cloud.client.close)

    def create_photo(self):
        return self.store.create('gallery', {'title': '现场留影', 'type': 'mcm_london'}, {'url': upload()})['id']

    def test_connection_check_uses_real_sdk_bucket_models(self):
        self.store.check()

    def test_pending_private_and_signed_admin_preview_only(self):
        item_id = self.create_photo()
        self.assertEqual(self.store.list('gallery'), [])
        row = self.store.list('gallery', 'pending')[0]
        self.assertEqual(row['id'], item_id)
        self.assertIn('/object/sign/imas-pending/', row['url'])
        self.assertEqual(row['preview_expires_in'], 900)
        self.assertNotIn('files', row)
        self.assertNotIn('token=', json.dumps(self.cloud.rows))
        self.assertEqual(len(self.cloud.objects['imas-pending']), 2)
        self.assertFalse(self.cloud.objects['imas-public'])
        with self.assertRaises(StoreError):
            self.store._serialize(self.cloud.rows[0])

    def test_approval_publishes_both_images_and_cleans_pending(self):
        item_id = self.create_photo()
        row = self.store.approve('gallery', item_id)
        self.assertTrue(row['approved'])
        self.assertIn('/object/public/imas-public/', row['url'])
        self.assertFalse(self.cloud.objects['imas-pending'])
        self.assertEqual(len(self.cloud.objects['imas-public']), 2)
        self.assertEqual(len(self.store.list('gallery')), 1)
        uploads = len(self.cloud.calls)
        self.store.approve('gallery', item_id)
        self.assertEqual(len(self.cloud.calls), uploads + 1)  # 已通过时只读记录

    def test_both_card_faces_validated_before_cloud_writes(self):
        with self.assertRaises(UploadError):
            self.store.create('business_cards', {'owner': 'P'}, {
                'front': upload(), 'back': FileStorage(stream=io.BytesIO(b'<script>bad</script>')),
            })
        self.assertEqual(self.cloud.calls, [])

    def test_card_upload_partial_failure_removes_first_face(self):
        original = self.cloud.handle
        count = 0
        def fail_second(req):
            nonlocal count
            if req.method == 'POST' and '/object/imas-pending/' in req.url.path:
                count += 1
                if count == 2:
                    return httpx.Response(500, json={'statusCode': '500', 'error': 'test', 'message': 'outage'})
            return original(req)
        self.cloud.client._transport = httpx.MockTransport(fail_second)
        with self.assertRaises(Exception):
            self.store.create('business_cards', {'owner': 'P'}, {'front': upload(), 'back': upload()})
        self.assertFalse(self.cloud.objects['imas-pending'])
        self.assertFalse(self.cloud.rows)

    def test_failed_database_insert_cleans_uploaded_files(self):
        self.cloud.error_once('POST', '/rest/v1/submissions')
        with self.assertRaises(Exception):
            self.create_photo()
        self.assertFalse(self.cloud.objects['imas-pending'])
        self.assertFalse(self.cloud.rows)

    def test_lost_insert_response_does_not_delete_committed_images(self):
        self.cloud.lose_insert_response = True
        item_id = self.create_photo()
        self.assertEqual(item_id, self.cloud.rows[0]['id'])
        self.assertEqual(len(self.cloud.objects['imas-pending']), 2)

    def test_quota_rejection_rolls_back_and_gives_readable_error(self):
        self.cloud.quota = True
        with self.assertRaisesRegex(UploadError, '配额'):
            self.create_photo()
        self.assertFalse(self.cloud.objects['imas-pending'])

    def test_failed_approval_update_unpublishes_copies(self):
        item_id = self.create_photo()
        self.cloud.error_once('PATCH', '/rest/v1/submissions')
        with self.assertRaises(Exception):
            self.store.approve('gallery', item_id)
        self.assertFalse(self.cloud.rows[0]['approved'])
        self.assertFalse(self.cloud.objects['imas-public'])
        self.assertEqual(len(self.cloud.objects['imas-pending']), 2)

    def test_failed_delete_can_be_retried_and_hides_record(self):
        item_id = self.create_photo()
        self.store.approve('gallery', item_id)
        self.cloud.error_once('DELETE', '/storage/v1/object/imas-public')
        with self.assertRaises(Exception):
            self.store.delete('gallery', item_id)
        self.assertTrue(self.cloud.rows[0]['deleting'])
        self.assertFalse(self.store.list('gallery'))
        self.assertTrue(self.store.delete('gallery', item_id))
        self.assertFalse(self.cloud.rows)
        self.assertFalse(self.cloud.objects['imas-public'])

    def test_pagination_does_not_truncate_records(self):
        item_id = self.create_photo()
        self.store.approve('gallery', item_id)
        seed = copy.deepcopy(self.cloud.rows[0])
        self.cloud.rows = [dict(seed, id=i) for i in range(1, 206)]
        self.assertEqual(len(self.store.list('gallery')), 205)

    def test_migration_dry_run_and_repeat_do_not_destroy_local_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'business_cards').mkdir()
            path = root / 'business_cards/front.png'
            path.write_bytes(picture().getvalue())
            record = {'id': 9, 'owner': 'P', 'approved': True,
                      'front': '/uploads/business_cards/front.png', 'back': '/uploads/business_cards/front.png'}
            self.assertEqual(self.store.import_local('business_cards', record, root), 'ready')
            self.assertFalse(self.cloud.rows)
            self.assertEqual(self.store.import_local('business_cards', record, root, True), 'imported')
            self.assertEqual(self.store.import_local('business_cards', record, root, True), 'skipped')
            self.assertTrue(path.is_file())
            self.assertEqual(len(self.cloud.rows), 1)


class FlaskAndLocalTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {'SECRET_KEY': 'test-secret-not-real', 'STORAGE_BACKEND': 'local'})
        self.env.start()
        self.addCleanup(self.env.stop)
        import app
        self.module = app
        self.client = app.app.test_client()

    def test_admin_auth_required_before_storage_access(self):
        with patch.object(self.module, 'get_store') as factory:
            self.assertEqual(self.client.get('/api/admin/gallery').status_code, 401)
            self.assertEqual(self.client.post('/api/admin/gallery/1/approve').status_code, 401)
            factory.assert_not_called()

    def test_cloud_outage_is_not_a_successful_empty_gallery(self):
        with patch.object(self.module, 'get_store', side_effect=RuntimeError('cloud unavailable')):
            with self.assertLogs(self.module.app.logger, 'ERROR'):
                response = self.client.get('/api/gallery')
            self.assertEqual(response.status_code, 503)
            self.assertFalse(response.json['success'])
            self.assertNotIn('cloud unavailable', response.get_data(as_text=True))

    def test_cloud_mode_disables_legacy_upload_route(self):
        with patch.dict(os.environ, {'STORAGE_BACKEND': 'supabase'}):
            self.assertEqual(self.client.get('/uploads/business_cards/test.png').status_code, 404)

    def test_missing_cloud_config_does_not_fallback_to_local(self):
        with patch.dict(os.environ, {'STORAGE_BACKEND': 'supabase', 'SUPABASE_URL': '',
                                    'SUPABASE_SECRET_KEY': '', 'SUPABASE_SERVICE_ROLE_KEY': ''}):
            get_store.cache_clear()
            with self.assertRaises(StoreError):
                get_store()
        get_store.cache_clear()

    def test_full_flask_cloud_gallery_lifecycle(self):
        from auth import issue_token
        cloud = CloudHTTP()
        self.addCleanup(cloud.client.close)
        store = SupabaseStore(cloud.sdk)
        headers = {'Authorization': 'Bearer ' + issue_token('admin')}
        with patch.object(self.module, 'get_store', return_value=store):
            response = self.client.post('/api/gallery', data={
                'title': 'MCM', 'type': 'mcm_london', 'photo': (picture(), 'photo.png'),
            })
            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.client.get('/api/gallery').json['data'], [])
            response = self.client.get('/api/admin/gallery', headers=headers)
            item = response.json['data'][0]
            self.assertIn('token=', item['url'])
            self.assertEqual(self.client.post(f'/api/admin/gallery/{item["id"]}/approve', headers=headers).status_code, 200)
            public = self.client.get('/api/gallery').json['data'][0]
            self.assertNotIn('token=', public['url'])
            self.assertEqual(self.client.delete(f'/api/admin/gallery/{item["id"]}', headers=headers).status_code, 200)
            self.assertEqual(self.client.get('/api/gallery').json['data'], [])

    def test_metadata_is_stripped_and_images_are_resized(self):
        source = io.BytesIO()
        exif = Image.Exif()
        exif[270] = 'private description'
        Image.new('RGB', (3000, 50), 'red').save(source, 'PNG', exif=exif)
        source.seek(0)
        prepared = prepare_image(FileStorage(stream=source), 'gallery', 'photo', True)
        with Image.open(io.BytesIO(prepared['image']['data'])) as decoded:
            self.assertEqual(decoded.width, 2560)
            self.assertFalse(decoded.getexif())
        with Image.open(io.BytesIO(prepared['thumbnail']['data'])) as decoded:
            self.assertLessEqual(decoded.width, 640)

    def test_vue_history_routes_and_unknown_api(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text('<html>SPA</html>', encoding='utf-8')
            with patch.object(self.module, 'FRONTEND_DIST', root):
                with self.client.get('/gallery') as response:
                    self.assertEqual(response.status_code, 200)
                with self.client.get('/admin/login') as response:
                    self.assertIn(b'SPA', response.data)
                self.assertEqual(self.client.get('/api/not-real').status_code, 404)
                self.assertEqual(self.client.get('/assets/missing.js').status_code, 404)
                self.assertEqual(self.client.get('/../backend/.env').status_code, 404)

    def test_local_store_keeps_compatibility(self):
        import uploads
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'gallery.json').write_text('[]', encoding='utf-8')
            with patch.object(uploads, 'UPLOAD_ROOT', root / 'uploads'):
                store = LocalStore(root)
                row = store.create('gallery', {'title': 'local'}, {'url': upload()})
                self.assertFalse(store.list('gallery'))
                store.approve('gallery', row['id'])
                self.assertEqual(len(store.list('gallery')), 1)
                self.assertTrue(store.delete('gallery', row['id']))
                self.assertFalse(list((root / 'uploads').rglob('*.png')))


if __name__ == '__main__':
    unittest.main()
