// 管理员令牌存取与带鉴权的请求封装。
const TOKEN_KEY = 'imas_admin_token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export async function login(username, password) {
  const r = await fetch('/api/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  const body = await r.json()
  if (!r.ok || !body.success) throw new Error(body.error || '登录失败')
  setToken(body.data.token)
  return body.data
}

/** 带 Bearer 令牌的请求；令牌失效时清除本地令牌并抛出 401 错误。 */
export async function adminFetch(url, options = {}) {
  const r = await fetch(url, {
    ...options,
    headers: { ...(options.headers || {}), Authorization: `Bearer ${getToken()}` },
  })
  if (r.status === 401) {
    clearToken()
    const err = new Error('登录已过期，请重新登录')
    err.status = 401
    throw err
  }
  const body = await r.json()
  if (!r.ok || !body.success) throw new Error(body.error || '请求失败')
  return body
}

export async function verifyToken() {
  if (!getToken()) return false
  try {
    await adminFetch('/api/admin/me')
    return true
  } catch {
    return false
  }
}

// ── 名片墙 ──
export const listCards = (status) =>
  adminFetch(`/api/admin/business-cards?status=${status}`).then((b) => b.data)

export const approveCard = (id) =>
  adminFetch(`/api/admin/business-cards/${id}/approve`, { method: 'POST' })

export const deleteCard = (id) =>
  adminFetch(`/api/admin/business-cards/${id}`, { method: 'DELETE' })

// ── 照片墙 ──
export const listPhotos = (status) =>
  adminFetch(`/api/admin/gallery?status=${status}`).then((b) => b.data)

export const approvePhoto = (id) =>
  adminFetch(`/api/admin/gallery/${id}/approve`, { method: 'POST' })

export const deletePhoto = (id) =>
  adminFetch(`/api/admin/gallery/${id}`, { method: 'DELETE' })
