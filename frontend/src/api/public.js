// 图片通过 Flask 校验后上传。浏览器无需也不应配置 Supabase 管理密钥。
export async function readResponse(response) {
  let body
  try {
    body = await response.json()
  } catch {
    throw new Error(response.status === 413
      ? '上传图片过大，单张请控制在 8 MB 以内。'
      : '服务器暂时不可用，请稍后重试。')
  }
  if (!response.ok || !body.success) {
    throw new Error(body.error || '请求失败，请稍后重试。')
  }
  return body
}

export async function publicRequest(url, options = {}) {
  let response
  try {
    response = await fetch(url, options)
  } catch {
    throw new Error('无法连接服务器，请检查网络后重试。')
  }
  return readResponse(response)
}
