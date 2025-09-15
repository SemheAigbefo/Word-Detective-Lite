const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function req(path: string, opts: RequestInit = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
    ...opts
  })
  const data = await res.json()
  if (!res.ok) throw data
  return data
}

export const api = {
  createGame: (mode: 'daily' | 'free') => req('/api/game', { method: 'POST', body: JSON.stringify({ mode }) }),
  submitGuess: (gameId: string, word: string) => req('/api/guess', { method: 'POST', body: JSON.stringify({ gameId, word }) }),
  getGame: (id: string) => req(`/api/game/${id}`),
  health: () => req('/api/health')
}
export default api
