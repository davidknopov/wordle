# Requirements Traceability Matrix

This document maps each requirement to its implementation and test coverage.

---

## Backend Requirements

| ID | Requirement | Implementation | Tests |
|----|-------------|----------------|-------|
| BE-1 | Create new game (word length 5-8) | `POST /games` in `main.py` | `test_api.py::TestCreateGame` (4 tests) |
| BE-2 | Submit guesses with feedback (green/yellow/gray) | `POST /games/{id}/guesses` in `main.py`, `feedback.py` | `test_api.py::TestSubmitGuess` (4 tests), `test_feedback.py` (11 tests) |
| BE-3 | Retrieve game state | `GET /games/{id}` in `main.py` | `test_api.py::TestGetGame` (3 tests) |
| BE-4 | Validate guesses are real words | `words.py::is_valid_word()` | `test_words.py::TestWordValidation` (4 tests), `test_api.py::test_submit_invalid_word` |
| BE-5 | Appropriate data storage | `store.py::GameStore` (in-memory dict) | Implicitly tested via API tests |

---

## Frontend Requirements

| ID | Requirement | Implementation | Tests |
|----|-------------|----------------|-------|
| FE-1 | Start new game with word length 5-8 | `App.jsx::startGame()`, length buttons | `App.test.jsx::Game Setup` (2 tests) |
| FE-2 | Enter guesses via on-screen keyboard | `Keyboard.jsx`, `App.jsx::handleKey()` | `Keyboard.test.jsx` (7 tests) |
| FE-3 | Enter guesses via physical keyboard | `App.jsx` keydown listener | `App.test.jsx::handles physical keyboard input` |
| FE-4 | See feedback (green/yellow/gray letters) | `GameGrid.jsx` with status classes | `GameGrid.test.jsx::applies correct status classes` |
| FE-5 | View guess history | `GameGrid.jsx` renders all guesses | `GameGrid.test.jsx::displays guess letters` |
| FE-6 | See when won or lost | `App.jsx` status messages | `App.test.jsx::Win/Lose States` |

---

## Game Rules

| ID | Rule | Implementation | Tests |
|----|------|----------------|-------|
| R-1 | Green = correct position | `LetterStatus.CORRECT` in `feedback.py` | `test_feedback.py::test_all_correct` |
| R-2 | Yellow = wrong position | `LetterStatus.PRESENT` in `feedback.py` | `test_feedback.py::test_anagram` |
| R-3 | Gray = not in word | `LetterStatus.ABSENT` in `feedback.py` | `test_feedback.py::test_all_absent` |
| R-4 | Answers never plural | `words.py` filters words ending in 's' | `test_words.py::test_target_not_plural` |
| R-5 | Duplicate letter handling | Two-pass algorithm in `feedback.py` | `test_feedback.py::TestFeedbackDuplicateLetters` (6 tests) |
| R-6 | Must be valid dictionary word | `is_valid_word()` check in `main.py` | `test_api.py::test_submit_invalid_word` |
| R-7 | N+1 guesses for N letters | `Game.max_guesses` property | `test_api.py::test_create_game_*` |
| R-8 | Multiple concurrent games | UUID-based game IDs in `store.py` | Implicitly tested via API tests |

---

## Test Summary

| Component | Test File | Tests | Status |
|-----------|-----------|-------|--------|
| Backend - Feedback Algorithm | `test_feedback.py` | 11 | ✅ Pass |
| Backend - Word Validation | `test_words.py` | 10 | ✅ Pass |
| Backend - API Endpoints | `test_api.py` | 13 | ✅ Pass |
| Frontend - GameGrid | `GameGrid.test.jsx` | 5 | ✅ Pass |
| Frontend - Keyboard | `Keyboard.test.jsx` | 7 | ✅ Pass |
| Frontend - App Integration | `App.test.jsx` | 6 | ✅ Pass |
| **Total** | | **52** | ✅ **All Pass** |

---

## Running Tests

### Backend
```bash
cd backend
source venv/bin/activate
pytest -v
```

### Frontend
```bash
cd frontend
npm test
```

### All Tests
```bash
# From project root
cd backend && source venv/bin/activate && pytest -v && cd ../frontend && npm test
```
