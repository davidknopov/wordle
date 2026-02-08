# Wordle Clone

A full-stack Wordle clone with configurable word lengths (5-8 letters).

## Project Structure

```
wordle/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── routes/
│   │   │   └── games.py         # Game API endpoints
│   │   ├── models/
│   │   │   ├── game.py          # Domain models (LetterStatus, Guess)
│   │   │   └── schemas.py       # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── feedback.py      # Two-pass feedback algorithm
│   │   │   ├── words.py         # Word validation and selection
│   │   │   └── game_service.py  # Game entity and repository
│   │   └── data/
│   │       └── words_*.txt      # Word lists by length
│   ├── tests/
│   │   ├── test_api.py          # API integration tests
│   │   ├── test_feedback.py     # Feedback algorithm unit tests
│   │   └── test_words.py        # Word service unit tests
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx              # Main application component
│       ├── App.test.jsx         # App integration tests
│       ├── api/
│       │   └── game.js          # API client functions
│       ├── hooks/
│       │   └── useKeyboard.js   # Keyboard input hook
│       └── components/
│           ├── GameGrid/        # Game board component
│           │   ├── index.jsx
│           │   ├── GameGrid.css
│           │   └── GameGrid.test.jsx
│           └── Keyboard/        # On-screen keyboard
│               ├── index.jsx
│               ├── Keyboard.css
│               └── Keyboard.test.jsx
├── docs/
│   ├── DESIGN.md                # Architecture and design decisions
│   ├── REQUIREMENTS.md          # Requirements traceability matrix
│   └── TODO.md                  # Future improvements
└── README.md
```

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Running Tests

### Backend (27 tests)
```bash
cd backend
source venv/bin/activate
PYTHONPATH=. pytest tests/ -v
```

### Frontend (18 tests)
```bash
cd frontend
npm test
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/games` | Create a new game |
| POST | `/games/{id}/guesses` | Submit a guess |
| GET | `/games/{id}` | Get game state |
| GET | `/health` | Health check |

## Features

- Configurable word length (5-8 letters)
- Dynamic max guesses (word_length + 1)
- Correct duplicate letter handling
- Responsive design (mobile + desktop)
- Physical and on-screen keyboard support
- Win/lose states with target reveal

## Documentation

- [Design Document](docs/DESIGN.md) - Architecture, tradeoffs, alternatives
- [Requirements](docs/REQUIREMENTS.md) - Test traceability matrix
- [TODO](docs/TODO.md) - Future improvements
