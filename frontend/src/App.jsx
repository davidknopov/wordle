import { useState, useEffect, useCallback } from 'react'
import './App.css'
import GameGrid from './components/GameGrid'
import Keyboard from './components/Keyboard'

const API_URL = 'http://localhost:8000'

function App() {
  const [gameId, setGameId] = useState(null)
  const [wordLength, setWordLength] = useState(5)
  const [maxGuesses, setMaxGuesses] = useState(6)
  const [guesses, setGuesses] = useState([])
  const [currentGuess, setCurrentGuess] = useState('')
  const [gameStatus, setGameStatus] = useState('idle')
  const [targetWord, setTargetWord] = useState(null)
  const [error, setError] = useState('')
  const [letterStatuses, setLetterStatuses] = useState({})

  const startGame = async (length) => {
    try {
      const res = await fetch(`${API_URL}/games`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word_length: length })
      })
      const data = await res.json()
      setGameId(data.id)
      setWordLength(data.word_length)
      setMaxGuesses(data.max_guesses)
      setGuesses([])
      setCurrentGuess('')
      setGameStatus('in_progress')
      setTargetWord(null)
      setError('')
      setLetterStatuses({})
    } catch (e) {
      setError('Failed to start game')
    }
  }

  const submitGuess = async () => {
    if (currentGuess.length !== wordLength) return
    
    try {
      const res = await fetch(`${API_URL}/games/${gameId}/guesses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: currentGuess })
      })
      
      if (!res.ok) {
        const err = await res.json()
        setError(err.detail)
        return
      }
      
      const data = await res.json()
      const newGuess = { word: data.word, feedback: data.feedback }
      setGuesses(prev => [...prev, newGuess])
      setCurrentGuess('')
      setError('')
      
      // Update letter statuses (best status wins)
      const priority = { correct: 3, present: 2, absent: 1 }
      setLetterStatuses(prev => {
        const updated = { ...prev }
        data.feedback.forEach(({ letter, status }) => {
          if (!updated[letter] || priority[status] > priority[updated[letter]]) {
            updated[letter] = status
          }
        })
        return updated
      })
      
      if (data.game_status !== 'in_progress') {
        setGameStatus(data.game_status)
        // Fetch final state to get target word
        const stateRes = await fetch(`${API_URL}/games/${gameId}`)
        const stateData = await stateRes.json()
        setTargetWord(stateData.target_word)
      }
    } catch (e) {
      setError('Failed to submit guess')
    }
  }

  const handleKey = useCallback((key) => {
    if (gameStatus !== 'in_progress') return
    
    setError('')
    
    if (key === 'Enter') {
      submitGuess()
    } else if (key === 'Backspace') {
      setCurrentGuess(prev => prev.slice(0, -1))
    } else if (/^[a-zA-Z]$/.test(key) && currentGuess.length < wordLength) {
      setCurrentGuess(prev => prev + key.toLowerCase())
    }
  }, [gameStatus, currentGuess, wordLength, submitGuess])

  useEffect(() => {
    const onKeyDown = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return
      handleKey(e.key)
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [handleKey])

  // Build display guesses (including current input)
  const displayGuesses = [...guesses]
  if (gameStatus === 'in_progress' && currentGuess) {
    displayGuesses.push({
      word: currentGuess,
      feedback: currentGuess.split('').map(letter => ({ letter, status: '' }))
    })
  }

  return (
    <div className="app">
      <h1>Wordle</h1>
      
      {gameStatus === 'idle' && (
        <div className="setup">
          <p>Select word length:</p>
          <div className="length-buttons">
            {[5, 6, 7, 8].map(n => (
              <button key={n} onClick={() => startGame(n)}>{n} letters</button>
            ))}
          </div>
        </div>
      )}
      
      {gameStatus !== 'idle' && (
        <>
          <GameGrid 
            guesses={displayGuesses} 
            wordLength={wordLength} 
            maxGuesses={maxGuesses} 
          />
          
          {error && <p className="error">{error}</p>}
          
          {gameStatus === 'won' && (
            <p className="message success">You won! 🎉</p>
          )}
          
          {gameStatus === 'lost' && (
            <p className="message failure">
              Game over! The word was: <strong>{targetWord?.toUpperCase()}</strong>
            </p>
          )}
          
          {gameStatus === 'in_progress' && (
            <Keyboard onKey={handleKey} letterStatuses={letterStatuses} />
          )}
          
          {gameStatus !== 'in_progress' && (
            <button className="new-game" onClick={() => setGameStatus('idle')}>
              New Game
            </button>
          )}
        </>
      )}
    </div>
  )
}

export default App
