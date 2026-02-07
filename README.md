# Wordle Clone

A full-stack Wordle implementation with configurable word lengths (5-8 letters), built with FastAPI and React.

## Features

- 🎮 **Multiple Games**: Create and play as many games as you want
- 📏 **Configurable Word Length**: Choose 5-8 letter words (with N+1 guesses)
- ⌨️ **Dual Input**: On-screen keyboard and physical keyboard support
- 🎨 **Responsive Design**: Works on desktop and mobile
- ✅ **52 Tests**: Comprehensive test coverage

## Quick Start

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
API available at http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App available at http://localhost:5173

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/games` | Create new game with `{word_length: 5-8}` |
| POST | `/games/{id}/guesses` | Submit guess, returns feedback |
| GET | `/games/{id}` | Get game state |

## Project Structure

```
wordle-starter/
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── models.py        # Pydantic schemas
│   ├── game.py          # Game model
│   ├── feedback.py      # Scoring algorithm
│   ├── words.py         # Word validation
│   ├── store.py         # Game storage
│   ├── test_*.py        # Backend tests (34)
│   └── words_*.txt      # Word lists
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main component
│   │   ├── components/  # GameGrid, Keyboard
│   │   └── test/        # Frontend tests (18)
│   └── package.json
├── DESIGN.md            # Architecture & tradeoffs
├── REQUIREMENTS.md      # Test traceability matrix
└── TODO.md              # Future improvements
```

## Running Tests

```bash
# Backend (34 tests)
cd backend && source venv/bin/activate && pytest -v

# Frontend (18 tests)
cd frontend && npm test

# All tests
cd backend && source venv/bin/activate && pytest && cd ../frontend && npm test
```

## Design Decisions

See [DESIGN.md](DESIGN.md) for detailed architecture documentation including:
- API design rationale
- Storage layer tradeoffs
- Feedback algorithm explanation
- Frontend state management choices

## Game Rules

1. 🟩 **Green** = Letter is correct and in the right position
2. 🟨 **Yellow** = Letter is in the word but wrong position  
3. ⬜ **Gray** = Letter is not in the word
4. Words must be valid English words
5. Answers are never plural
6. You get N+1 guesses for an N-letter word

## Tech Stack

- **Backend**: Python, FastAPI, Pydantic
- **Frontend**: React, Vite, Vitest
- **Testing**: pytest, React Testing Library
