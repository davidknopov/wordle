const API_BASE = 'http://localhost:8000'

export async function createGame(wordLength) {
  const res = await fetch(`${API_BASE}/games`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ word_length: wordLength }),
  })
  if (!res.ok) throw new Error('Failed to create game')
  return res.json()
}

export async function submitGuess(gameId, word) {
  const res = await fetch(`${API_BASE}/games/${gameId}/guesses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ word }),
  })
  return { ok: res.ok, data: await res.json() }
}
