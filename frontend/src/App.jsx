import { useState, useCallback } from 'react'
import './App.css'
import GameGrid from './components/GameGrid'
import Keyboard from './components/Keyboard'
import { createGame, submitGuess, getGame } from './api'
import { useKeyboard } from './hooks'

const STATUS_PRIORITY = { correct: 3, present: 2, absent: 1 }

function App() {
  const [game, setGame] = useState(null)
  const [guesses, setGuesses] = useState([])
  const [currentGuess, setCurrentGuess] = useState('')
  const [gameStatus, setGameStatus] = useState('idle')
  const [targetWord, setTargetWord] = useState(null)
  const [error, setError] = useState('')
  const [letterStatuses, setLetterStatuses] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const startGame = async (length) => {
    try {
      const data = await createGame(length)
      setGame(data)
      setGuesses([])
      setCurrentGuess('')
      setGameStatus('in_progress')
      setTargetWord(null)
      setError('')
      setLetterStatuses({})
    } catch {
      setError('Failed to start game')
    }
  }

  const handleSubmit = useCallback(async () => {
    if (!game || currentGuess.length !== game.word_length || isSubmitting) return
    
    setIsSubmitting(true)
    try {
      const { ok, data } = await submitGuess(game.id, currentGuess)
      
      if (!ok) {
        setError(data.detail)
        return
      }
      
      setGuesses(prev => [...prev, { word: data.word, feedback: data.feedback }])
      setCurrentGuess('')
      setError('')
      
      // Update letter statuses (best status wins)
      setLetterStatuses(prev => {
        const updated = { ...prev }
        data.feedback.forEach(({ letter, status }) => {
          if (!updated[letter] || STATUS_PRIORITY[status] > STATUS_PRIORITY[updated[letter]]) {
            updated[letter] = status
          }
        })
        return updated
      })
      
      if (data.game_status !== 'in_progress') {
        setGameStatus(data.game_status)
        const state = await getGame(game.id)
        setTargetWord(state.target_word)
      }
    } catch {
      setError('Failed to submit guess')
    } finally {
      setIsSubmitting(false)
    }
  }, [game, currentGuess, isSubmitting])

  const handleKey = useCallback((key) => {
    if (gameStatus !== 'in_progress' || !game || isSubmitting) return
    setError('')
    
    if (key === 'Enter') {
      handleSubmit()
    } else if (key === 'Backspace') {
      setCurrentGuess(prev => prev.slice(0, -1))
    } else if (/^[a-z]$/.test(key) && currentGuess.length < game.word_length) {
      setCurrentGuess(prev => prev + key)
    }
  }, [gameStatus, game, currentGuess, isSubmitting, handleSubmit])

  useKeyboard(handleKey, gameStatus === 'in_progress' && !isSubmitting)

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
      
      {game && gameStatus !== 'idle' && (
        <>
          <GameGrid 
            guesses={displayGuesses} 
            wordLength={game.word_length} 
            maxGuesses={game.max_guesses} 
          />
          
          {error && <p className="error">{error}</p>}
          
          {gameStatus === 'won' && <p className="message success">You won! 🎉</p>}
          
          {gameStatus === 'lost' && (
            <p className="message failure">
              Game over! The word was: <strong>{targetWord?.toUpperCase()}</strong>
            </p>
          )}
          
          {gameStatus === 'in_progress' && (
            <Keyboard onKey={handleKey} letterStatuses={letterStatuses} disabled={isSubmitting} />
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
