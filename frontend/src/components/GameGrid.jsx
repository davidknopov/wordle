import './GameGrid.css'

export default function GameGrid({ guesses, wordLength, maxGuesses }) {
  const rows = []
  
  for (let i = 0; i < maxGuesses; i++) {
    const guess = guesses[i]
    const cells = []
    
    for (let j = 0; j < wordLength; j++) {
      const feedback = guess?.feedback[j]
      const letter = feedback?.letter || ''
      const status = feedback?.status || ''
      
      cells.push(
        <div key={j} className={`cell ${status}`}>
          {letter.toUpperCase()}
        </div>
      )
    }
    
    rows.push(
      <div key={i} className="row">
        {cells}
      </div>
    )
  }
  
  return (
    <div className="grid" style={{ '--word-length': wordLength }}>
      {rows}
    </div>
  )
}
