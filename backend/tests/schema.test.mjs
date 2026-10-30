// 用法：node backend/tests/schema.test.mjs <@electric-sql/pglite/dist/index.js 的路径>
// 验证真实 PostgreSQL DDL、权限和配额触发器；不连接用户的 Supabase。
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'

if (!process.argv[2]) throw new Error('请提供临时安装的 PGlite 模块路径')
const { PGlite } = await import(pathToFileURL(process.argv[2]).href)
const db = new PGlite()
try {
  // Supabase 预置的角色和桶表，仅在测试数据库内模拟。
  await db.exec(`
    create role anon;
    create role authenticated;
    create role service_role bypassrls;
    create schema storage;
    create table storage.buckets (
      id text primary key, name text not null, public boolean not null,
      file_size_limit bigint, allowed_mime_types text[]
    );
  `)
  const sql = await readFile(new URL('../supabase/schema.sql', import.meta.url), 'utf8')
  await db.exec(sql)
  const insert = `insert into public.submissions (kind,payload,files,size_bytes)
    values ('gallery','{"title":"test"}','{"url":"gallery/test.png"}',10)`
  await db.exec(insert)
  await db.exec(sql)
  assert.equal((await db.query('select count(*)::int as n from public.submissions')).rows[0].n, 1)
  const buckets = (await db.query('select id,public from storage.buckets order by id')).rows
  assert.deepEqual(buckets, [{ id: 'imas-pending', public: false }, { id: 'imas-public', public: true }])

  await db.exec('set role anon')
  await assert.rejects(db.query('select * from public.submissions'), /permission denied/)
  await db.exec('reset role; set role authenticated')
  await assert.rejects(db.query('select * from public.submissions'), /permission denied/)
  await db.exec('reset role; set role service_role')
  assert.equal((await db.query('select count(*)::int as n from public.submissions')).rows[0].n, 1)
  await db.exec('update public.media_settings set max_bytes=15 where id=true')
  await assert.rejects(db.exec(insert), /media_storage_quota_exceeded/)
  // 审核状态修改不增加文件体积；服务端角色仍然受容量触发器约束。
  await db.exec('update public.submissions set approved=true')
  await assert.rejects(db.exec('update public.submissions set size_bytes=16'), /media_storage_quota_exceeded/)
  await db.exec('delete from public.submissions')
  await db.exec(insert)
  console.log('SQL checks passed: repeatable setup, private/public buckets, role permissions, quota rejection, delete frees quota.')
} finally {
  await db.close()
}
