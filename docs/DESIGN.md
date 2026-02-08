# Wordle Clone - Architecture & Design Document

## Overview

A full-stack Wordle implementation with configurable word lengths (5-8 letters), supporting multiple concurrent games. Built with FastAPI (Python) backend and React (Vite) frontend.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   App.jsx   │  │  GameGrid/  │  │       Keyboard/         │  │
│  │  (state +   │  │  (display)  │  │  (input + status)       │  │
│  │   logic)    │  │             │  │                         │  │
│  └──────┬──────┘  └─────────────┘  └─────────────────────────┘  │
│         │                                                        │
│  ┌──────┴──────┐  ┌─────────────┐                               │
│  │   api/      │  │   hooks/    │                               │
│  │  (HTTP)     │  │ (keyboard)  │                               │
│  └──────┬──────┘  └─────────────┘                               │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ▼ HTTP (fetch)
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  app/                                                        ││
│  │  ├── main.py          (FastAPI app + middleware)            ││
│  │  ├── routes/                                                 ││
│  │  │   └── games.py     (API endpoints)                       ││
│  │  ├── models/                                                 ││
│  │  │   ├── game.py      (domain: LetterStatus, Guess)         ││
│  │  │   └── schemas.py   (Pydantic request/response)           ││
│  │  ├── services/                                               ││
│  │  │   ├── feedback.py  (scoring algorithm)                   ││
│  │  │   ├── words.py     (validation + selection)              ││
│  │  │   └── game_service.py (Game entity + Repository)         ││
│  │  └── data/                                                   ││
│  │      └── words_*.txt  (embedded word lists)                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## API Design

### Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/games` | Create new game |
| POST | `/games/{id}/guesses` | Submit a guess |
| GET | `/games/{id}` | Get game state |
| GET | `/health` | Health check |

### Design Principles

1. **RESTful Resources**: Games are resources, guesses are sub-resources
2. **Stateless Requests**: All state stored server-side, referenced by game ID
3. **Consistent Response Shapes**: Pydantic models enforce schema consistency
4. **Appropriate HTTP Status Codes**: 200 (success), 400 (bad request), 404 (not found)

### Alternative Considered: WebSockets

| Approach | Pros | Cons |
|----------|------|------|
| **REST (chosen)** | Simple, stateless, cacheable, easy to debug | Polling needed for multiplayer |
| **WebSocket** | Real-time updates, lower latency | Complexity, connection management, overkill for single-player |

**Decision**: REST is appropriate for a turn-based single-player game. WebSockets would be warranted for real-time multiplayer.

---

## Data Model

```python
Game:
  id: str (UUID)
  word_length: int (5-8)
  target_word: str
  guesses: list[Guess]
  status: "in_progress" | "won" | "lost"

Guess:
  word: str
  feedback: list[LetterFeedback]

LetterFeedback:
  letter: str
  status: "correct" | "present" | "absent"
```

### Design Decisions

1. **Computed Properties**: `max_guesses` and `guesses_remaining` are computed from `word_length` and `len(guesses)` - single source of truth
2. **Target Word Hidden**: Only revealed in API response when game is over
3. **Immutable Guesses**: Once submitted, guesses cannot be modified

---

## Storage Layer

### Chosen: In-Memory Dictionary

```python
class GameStore:
    def __init__(self):
        self._games: dict[str, Game] = {}
    
    def save(self, game: Game) -> None
    def get(self, game_id: str) -> Game | None
```

### Tradeoffs

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **In-Memory (chosen)** | Simple, fast, no dependencies | Lost on restart, no horizontal scaling | Toy/demo, single instance |
| **SQLite** | Persistent, still simple, no server | File locking, limited concurrency | Small production, single instance |
| **Redis** | Fast, persistent, TTL support | External dependency | Production, need expiration |
| **PostgreSQL** | ACID, scalable, queryable | Complexity, operational overhead | Production, need analytics |

**Decision**: In-memory is appropriate for an assessment. The `GameStore` abstraction allows easy swap to persistent storage later.

**Production Evolution Path**:
```
In-Memory → Redis (add persistence + TTL) → PostgreSQL (add analytics)
```

---

## Word List Strategy

### Chosen: Embedded Word Lists

```
backend/
  words_5.txt (12,971 words)
  words_6.txt (29,874 words)
  words_7.txt (41,998 words)
  words_8.txt (51,627 words)
```

### Tradeoffs

| Approach | Pros | Cons |
|----------|------|------|
| **Embedded lists (chosen)** | Fast, offline, reliable, no API limits | Bundled size (~2MB), manual updates |
| **External Dictionary API** | Always current, smaller bundle | Latency, rate limits, dependency, offline broken |
| **Database lookup** | Queryable, updatable | Slower, more complex |

**Decision**: Embedded lists match what the real Wordle does. Instant validation, no network dependency, predictable behavior.

### Word Selection

- **Valid Guesses**: All words in list (~13k for 5-letter)
- **Target Words**: Filtered to exclude plurals (words ending in 's')

**Why filter plurals?** The spec says "Answers are never plural." This improves gameplay - players don't need to guess between WORD and WORDS.

---

## Feedback Algorithm

### The Challenge: Duplicate Letters

Naive approach fails for words with repeated letters.

**Example**: Target = `APPLE`, Guess = `PAPER`

### Chosen: Two-Pass Algorithm

```python
def compute_feedback(guess: str, target: str) -> list[LetterFeedback]:
    # Pass 1: Mark exact matches (green)
    # - Consume matched target letters
    
    # Pass 2: Mark present (yellow) or absent (gray)
    # - Only match against remaining target letters
    # - Consume on match to prevent double-counting
```

**Why two passes?**
1. Greens take priority - if a letter is in the right spot, it shouldn't also trigger a yellow elsewhere
2. Prevents over-counting - each target letter can only satisfy one guess letter

### Alternative: Single Pass with Post-Processing

Could mark all matches then adjust, but two-pass is clearer and matches how humans think about the problem.

---

## Frontend Architecture

### State Management: React useState

```javascript
const [gameId, setGameId] = useState(null)
const [guesses, setGuesses] = useState([])
const [currentGuess, setCurrentGuess] = useState('')
const [gameStatus, setGameStatus] = useState('idle')
const [letterStatuses, setLetterStatuses] = useState({})
```

### Tradeoffs

| Approach | Pros | Cons |
|----------|------|------|
| **useState (chosen)** | Simple, built-in, sufficient for this scope | Can get messy with many states |
| **useReducer** | Better for complex state logic | More boilerplate |
| **Redux/Zustand** | Scalable, devtools, middleware | Overkill for single-component app |
| **Server State (React Query)** | Caching, sync, optimistic updates | Additional dependency |

**Decision**: `useState` is appropriate. State is localized to one component, no complex transitions, no shared state needs.

### Keyboard Handling

Dual input support:
1. **Physical keyboard**: `window.addEventListener('keydown', ...)`
2. **On-screen keyboard**: `onClick` handlers

Both funnel through single `handleKey` function for consistency.

---

## Responsive Design

### Approach: CSS-First with clamp() and min()

```css
.cell {
  --cell-size: min(52px, calc((100vw - 60px) / var(--word-length)));
  width: var(--cell-size);
  height: var(--cell-size);
}
```

### Why CSS Variables?

- Grid cell size depends on `word_length` (5-8)
- CSS variable passed from React: `style={{ '--word-length': wordLength }}`
- Enables pure CSS responsive calculation

### Tradeoffs

| Approach | Pros | Cons |
|----------|------|------|
| **CSS clamp/min (chosen)** | No JS, smooth scaling, performant | Limited logic |
| **JS resize listener** | Full control | Complexity, potential jank |
| **Fixed breakpoints** | Predictable | Jumpy transitions |

---

## Error Handling

### Backend

| Error | HTTP Status | Response |
|-------|-------------|----------|
| Game not found | 404 | `{"detail": "Game not found"}` |
| Invalid word | 400 | `{"detail": "Not a valid word"}` |
| Wrong length | 400 | `{"detail": "Word must be N letters"}` |
| Game over | 400 | `{"detail": "Game is already over"}` |
| Invalid params | 422 | Pydantic validation error |

### Frontend

- Displays error messages inline
- Clears error on next valid action
- Graceful degradation if API unreachable

---

## Security Considerations

### Current (Assessment Scope)

- CORS configured for localhost only
- No authentication (games are anonymous)
- No rate limiting

### Production Additions

1. **Rate Limiting**: Prevent brute-force guessing
2. **Input Validation**: Already handled by Pydantic
3. **Game Expiration**: TTL on games to prevent memory exhaustion
4. **HTTPS**: Required for production

---

## Testing Strategy

### What Would Be Added for Production

| Layer | Tool | Coverage |
|-------|------|----------|
| Unit | pytest | Feedback algorithm, word validation |
| API | pytest + httpx | Endpoint contracts, error cases |
| Frontend | Vitest + Testing Library | Component rendering, user interactions |
| E2E | Playwright | Full game flow |

### Critical Test Cases

1. Feedback algorithm with duplicate letters
2. Win/lose detection
3. Invalid word rejection
4. Word length boundaries (5 and 8)
5. Game state persistence across requests

---

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Word validation | O(1) | Set lookup |
| Feedback computation | O(n) | n = word length |
| Game retrieval | O(1) | Dict lookup |
| Word list loading | O(n) | Once per word length, lazy loaded |

### Memory Usage

- Word lists: ~2MB total (loaded lazily)
- Per game: ~1KB
- 10,000 concurrent games: ~10MB

---

## Future Enhancements

### If This Were Production

1. **User Accounts**: Track statistics, streaks
2. **Daily Challenge**: Shared word of the day
3. **Multiplayer**: Race mode, head-to-head
4. **Hints System**: Reveal a letter
5. **Hard Mode**: Must use confirmed letters
6. **Analytics**: Popular guesses, win rates by word length
7. **Accessibility**: Screen reader support, high contrast mode

---

## Summary

This implementation prioritizes:

1. **Correctness**: Proper duplicate letter handling, rule compliance
2. **Simplicity**: Minimal dependencies, clear separation of concerns
3. **Extensibility**: Storage abstraction, clean API contracts
4. **User Experience**: Responsive design, dual input methods, clear feedback

The architecture is intentionally simple for the assessment scope while demonstrating awareness of production considerations through abstractions and documented tradeoffs.
