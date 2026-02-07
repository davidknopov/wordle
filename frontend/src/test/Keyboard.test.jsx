import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import Keyboard from '../components/Keyboard'

describe('Keyboard', () => {
  it('renders all letter keys', () => {
    render(<Keyboard onKey={() => {}} letterStatuses={{}} />)
    
    // Keys are lowercase in the component
    'qwertyuiopasdfghjklzxcvbnm'.split('').forEach(letter => {
      expect(screen.getByText(letter)).toBeInTheDocument()
    })
  })

  it('renders Enter and Backspace keys', () => {
    render(<Keyboard onKey={() => {}} letterStatuses={{}} />)
    
    expect(screen.getByText('Enter')).toBeInTheDocument()
    expect(screen.getByText('⌫')).toBeInTheDocument()
  })

  it('calls onKey with letter when clicked', () => {
    const onKey = vi.fn()
    render(<Keyboard onKey={onKey} letterStatuses={{}} />)
    
    fireEvent.click(screen.getByText('a'))
    expect(onKey).toHaveBeenCalledWith('a')
  })

  it('calls onKey with Enter when Enter clicked', () => {
    const onKey = vi.fn()
    render(<Keyboard onKey={onKey} letterStatuses={{}} />)
    
    fireEvent.click(screen.getByText('Enter'))
    expect(onKey).toHaveBeenCalledWith('Enter')
  })

  it('calls onKey with Backspace when ⌫ clicked', () => {
    const onKey = vi.fn()
    render(<Keyboard onKey={onKey} letterStatuses={{}} />)
    
    fireEvent.click(screen.getByText('⌫'))
    expect(onKey).toHaveBeenCalledWith('Backspace')
  })

  it('applies correct status class to keys', () => {
    const letterStatuses = {
      c: 'correct',
      r: 'present',
      a: 'absent',
    }
    render(<Keyboard onKey={() => {}} letterStatuses={letterStatuses} />)
    
    expect(screen.getByText('c')).toHaveClass('correct')
    expect(screen.getByText('r')).toHaveClass('present')
    expect(screen.getByText('a')).toHaveClass('absent')
  })

  it('keys without status have no status class', () => {
    render(<Keyboard onKey={() => {}} letterStatuses={{}} />)
    
    const keyQ = screen.getByText('q')
    expect(keyQ).not.toHaveClass('correct')
    expect(keyQ).not.toHaveClass('present')
    expect(keyQ).not.toHaveClass('absent')
  })
})
