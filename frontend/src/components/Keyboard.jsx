import './Keyboard.css'

const ROWS = [
  ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
  ['Enter', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '⌫']
]

export default function Keyboard({ onKey, letterStatuses }) {
  return (
    <div className="keyboard">
      {ROWS.map((row, i) => (
        <div key={i} className="keyboard-row">
          {row.map((key) => {
            const status = letterStatuses[key.toLowerCase()] || ''
            const isWide = key === 'Enter' || key === '⌫'
            return (
              <button
                key={key}
                className={`key ${status} ${isWide ? 'wide' : ''}`}
                onClick={() => onKey(key === '⌫' ? 'Backspace' : key)}
              >
                {key}
              </button>
            )
          })}
        </div>
      ))}
    </div>
  )
}
