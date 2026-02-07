import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from '../App'

// Mock fetch
global.fetch = vi.fn()

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Game Setup', () => {
    it('shows word length selection on initial load', () => {
      render(<App />)
      
      expect(screen.getByText('Select word length:')).toBeInTheDocument()
      expect(screen.getByText('5 letters')).toBeInTheDocument()
      expect(screen.getByText('6 letters')).toBeInTheDocument()
      expect(screen.getByText('7 letters')).toBeInTheDocument()
      expect(screen.getByText('8 letters')).toBeInTheDocument()
    })

    it('creates game when word length button clicked', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          id: 'test-game-id',
          word_length: 5,
          max_guesses: 6,
          status: 'in_progress'
        })
      })

      render(<App />)
      fireEvent.click(screen.getByText('5 letters'))

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/games',
          expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({ word_length: 5 })
          })
        )
      })
    })
  })

  describe('Game Play', () => {
    beforeEach(async () => {
      // Setup: create a game
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          id: 'test-game-id',
          word_length: 5,
          max_guesses: 6,
          status: 'in_progress'
        })
      })
    })

    it('shows game grid after starting game', async () => {
      render(<App />)
      fireEvent.click(screen.getByText('5 letters'))

      await waitFor(() => {
        const grid = document.querySelector('.grid')
        expect(grid).toBeInTheDocument()
      })
    })

    it('shows keyboard after starting game', async () => {
      render(<App />)
      fireEvent.click(screen.getByText('5 letters'))

      await waitFor(() => {
        const keyboard = document.querySelector('.keyboard')
        expect(keyboard).toBeInTheDocument()
      })
    })

    it('handles physical keyboard input', async () => {
      render(<App />)
      fireEvent.click(screen.getByText('5 letters'))

      await waitFor(() => {
        expect(document.querySelector('.grid')).toBeInTheDocument()
      })

      // Type a letter
      fireEvent.keyDown(window, { key: 'c' })
      
      // The letter should appear in the grid
      await waitFor(() => {
        expect(screen.getByText('C')).toBeInTheDocument()
      })
    })
  })

  describe('Win/Lose States', () => {
    it('shows win message when game won', async () => {
      // Create game
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          id: 'test-game-id',
          word_length: 5,
          max_guesses: 6,
          status: 'in_progress'
        })
      })

      render(<App />)
      fireEvent.click(screen.getByText('5 letters'))

      await waitFor(() => {
        expect(document.querySelector('.grid')).toBeInTheDocument()
      })

      // Mock winning guess
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          word: 'crane',
          feedback: [
            { letter: 'c', status: 'correct' },
            { letter: 'r', status: 'correct' },
            { letter: 'a', status: 'correct' },
            { letter: 'n', status: 'correct' },
            { letter: 'e', status: 'correct' },
          ],
          game_status: 'won',
          guesses_remaining: 5
        })
      })

      // Mock get game state
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          id: 'test-game-id',
          target_word: 'crane',
          status: 'won'
        })
      })

      // Type and submit
      'crane'.split('').forEach(letter => {
        fireEvent.keyDown(window, { key: letter })
      })
      fireEvent.keyDown(window, { key: 'Enter' })

      await waitFor(() => {
        expect(screen.getByText(/You won/)).toBeInTheDocument()
      })
    })
  })
})
