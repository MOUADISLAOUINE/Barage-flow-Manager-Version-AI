/**
 * services/api.js
 * Axios instance with JWT injection and error handling.
 */
import axios from 'axios'
import useAuthStore from '../store/authStore'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 15000,
})

// Attach JWT to every request
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Handle 401 — token expired
api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api


// ── Auth ────────────────────────────────────────────────────────────
export const authApi = {
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  verifyMfa: (mfaCode) =>
    api.post('/auth/mfa/verify', { totp_code: mfaCode }),
  logout: () => api.post('/auth/logout'),
}

// ── Dam ─────────────────────────────────────────────────────────────
export const damApi = {
  getStatus: (damId = 1) => api.get(`/dam/status?dam_id=${damId}`),
  updateThreshold: (damId, pct) =>
    api.patch(`/dam/thresholds?dam_id=${damId}&safety_reserve_pct=${pct}`),
}

// ── Sensors ─────────────────────────────────────────────────────────
export const sensorApi = {
  list: (damId = 1) => api.get(`/sensors/?dam_id=${damId}`),
  ingestReading: (data) => api.post('/sensors/readings', data),
}

// ── Cooperatives ────────────────────────────────────────────────────
export const cooperativeApi = {
  list: () => api.get('/cooperatives/'),
  get: (id) => api.get(`/cooperatives/${id}`),
}

// ── Release Orders ───────────────────────────────────────────────────
export const orderApi = {
  list: () => api.get('/release-orders/'),
  submit: (data) => api.post('/release-orders/', data),
  approve: (id, notes) => api.patch(`/release-orders/${id}/approve`, { notes }),
  reject: (id, notes) => api.patch(`/release-orders/${id}/reject`, { notes }),
  override: (id, mfaCode, justification) =>
    api.post(`/release-orders/${id}/override`, {
      mfa_code: mfaCode,
      justification,
    }),
}

// ── Forecast ────────────────────────────────────────────────────────
export const forecastApi = {
  getLatest: (damId = 1) => api.get(`/forecast/latest?dam_id=${damId}`),
}

// ── Admin (User Management) ───────────────────────────────────────────
export const adminApi = {
  listUsers: () => api.get('/users/'),
  createUser: (data) => api.post('/users/', data),
  updateUser: (id, data) => api.patch(`/users/${id}`, data),
  deleteUser: (id) => api.delete(`/users/${id}`),
  health: () => api.get('/admin/health'),
}
