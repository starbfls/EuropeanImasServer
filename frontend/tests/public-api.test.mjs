import test from 'node:test'
import assert from 'node:assert/strict'
import { publicRequest, readResponse } from '../src/api/public.js'

test('cloud outage stays an error instead of an empty list', async () => {
  const response = new Response(JSON.stringify({ success: false, error: '云端暂不可用' }), { status: 503 })
  await assert.rejects(readResponse(response), /云端暂不可用/)
})

test('reverse proxy HTML errors produce readable messages', async () => {
  await assert.rejects(readResponse(new Response('<html>bad gateway</html>', { status: 502 })), /服务器暂时不可用/)
  await assert.rejects(readResponse(new Response('<html>too large</html>', { status: 413 })), /8 MB/)
})

test('successful response retains cloud image URLs', async () => {
  const result = { success: true, data: [{ url: 'https://example.supabase.co/storage/v1/object/public/image.png' }] }
  assert.deepEqual(await readResponse(new Response(JSON.stringify(result))), result)
})

test('network failure is readable and does not retry uploads automatically', async () => {
  const previous = globalThis.fetch
  let calls = 0
  globalThis.fetch = async () => { calls++; throw new TypeError('offline') }
  try {
    await assert.rejects(publicRequest('/api/gallery', { method: 'POST' }), /无法连接服务器/)
    assert.equal(calls, 1)
  } finally {
    globalThis.fetch = previous
  }
})
