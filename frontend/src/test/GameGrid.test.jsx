import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import GameGrid from '../components/GameGrid'

describe('GameGrid', () => {
  it('renders correct number of rows based on maxGuesses', () => {
    render(<GameGrid guesses={[]} wordLength={5} maxGuesses={6} />)
    const rows = document.querySelectorAll('.row')
    expect(rows).toHaveLength(6)
  })

  it('renders correct number of cells per row based on wordLength', () => {
    render(<GameGrid guesses={[]} wordLength={7} maxGuesses={8} />)
    const firstRow = document.querySelector('.row')
    const cells = firstRow.querySelectorAll('.cell')
    expect(cells).toHaveLength(7)
  })

  it('displays guess letters in cells', () => {
    const guesses = [{
      word: 'crane',
      feedback: [
        { letter: 'c', status: 'absent' },
        { letter: 'r', status: 'present' },
        { letter: 'a', status: 'correct' },
        { letter: 'n', status: 'absent' },
        { letter: 'e', status: 'present' },
      ]
    }]
    render(<GameGrid guesses={guesses} wordLength={5} maxGuesses={6} />)
    
    expect(screen.getByText('C')).toBeInTheDocument()
    expect(screen.getByText('R')).toBeInTheDocument()
    expect(screen.getByText('A')).toBeInTheDocument()
    expect(screen.getByText('N')).toBeInTheDocument()
    expect(screen.getByText('E')).toBeInTheDocument()
  })

  it('applies correct status classes to cells', () => {
    const guesses = [{
      word: 'crane',
      feedback: [
        { letter: 'c', status: 'absent' },
        { letter: 'r', status: 'present' },
        { letter: 'a', status: 'correct' },
        { letter: 'n', status: 'absent' },
        { letter: 'e', status: 'present' },
      ]
    }]
    render(<GameGrid guesses={guesses} wordLength={5} maxGuesses={6} />)
    
    const cells = document.querySelectorAll('.row:first-child .cell')
    expect(cells[0]).toHaveClass('absent')
    expect(cells[1]).toHaveClass('present')
    expect(cells[2]).toHaveClass('correct')
    expect(cells[3]).toHaveClass('absent')
    expect(cells[4]).toHaveClass('present')
  })

  it('renders empty cells for remaining guesses', () => {
    render(<GameGrid guesses={[]} wordLength={5} maxGuesses={6} />)
    const cells = document.querySelectorAll('.cell')
    cells.forEach(cell => {
      expect(cell.textContent).toBe('')
    })
  })
})
