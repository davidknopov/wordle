# Wordle Clone

A full-stack Wordle implementation with configurable word lengths (5-8 letters).

**[Live Demo](http://localhost:5173)** | **[Design Doc](docs/DESIGN.md)** | **[Requirements](docs/REQUIREMENTS.md)**

---

## Quick Start

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

Open http://localhost:5173

---

## Architecture

```
backend/app/
├── routes/games.py      # API endpoints
├── services/
│   ├── feedback.py      # Two-pass scoring algorithm
│   ├── words.py         # Validation + random selection
│   └── game_service.py  # Game entity + Repository
└── models/              # Pydantic schemas

frontend/src/
├── api/                 # HTTP client
├── hooks/               # useKeyboard
└── components/          # GameGrid, Keyboard (co-located tests)
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **In-memory storage** | Appropriate for assessment; Repository pattern allows easy swap to Redis/Postgres |
| **Embedded word lists** | Fast, reliable, matches real Wordle (no external API dependency) |
| **Two-pass feedback** | Correctly handles duplicate letters (greens first, then yellows) |
| **REST over WebSocket** | Sufficient for turn-based single-player; WebSocket warranted for multiplayer |

See [DESIGN.md](docs/DESIGN.md) for full tradeoff analysis.

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/games` | Create game (word_length: 5-8) |
| POST | `/games/{id}/guesses` | Submit guess → feedback |
| GET | `/games/{id}` | Get game state |

---

## Tests

```bash
# Backend (27 tests)
cd backend && PYTHONPATH=. pytest tests/ -v

# Frontend (18 tests)
cd frontend && npm test
```

**45 tests total** covering feedback algorithm, API contracts, and UI components.

---

## What's Intentionally Deferred

| Item | Rationale |
|------|-----------|
| TypeScript | Starter was JS; conversion adds risk without functional benefit |
| E2E tests | Unit + integration cover correctness; E2E for production confidence |
| Auth/persistence | In-memory sufficient for demo; abstractions allow easy extension |

See [TODO.md](docs/TODO.md) for production roadmap.
