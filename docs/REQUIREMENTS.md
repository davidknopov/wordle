# Requirements Traceability Matrix

This document maps each requirement to its implementation and test coverage.

---

## Backend Requirements

| ID | Requirement | Implementation | Tests |
|----|-------------|----------------|-------|
| BE-1 | Create new game (word length 5-8) | `POST /games` in `routes/games.py` | `test_api.py::TestCreateGame` (4 tests) |
| BE-2 | Submit guesses with feedback | `POST /games/{id}/guesses`, `services/feedback.py` | `test_api.py::TestSubmitGuess` (4 tests), `test_feedback.py` (8 tests) |
| BE-3 | Retrieve game state | `GET /games/{id}` in `routes/games.py` | `test_api.py::TestGetGame` (3 tests) |
| BE-4 | Validate guesses are real words | `services/words.py::is_valid_word()` | `test_words.py` (7 tests) |
| BE-5 | Appropriate data storage | `services/game_service.py::GameRepository` | Implicitly tested via API tests |

---

## Frontend Requirements

| ID | Requirement | Implementation | Tests |
|----|-------------|----------------|-------|
| FE-1 | Start new game with word length 5-8 | `App.jsx::startGame()`, length buttons | `App.test.jsx::Game Setup` (2 tests) |
| FE-2 | Enter guesses via on-screen keyboard | `Keyboard/index.jsx`, `App.jsx::handleKey()` | `Keyboard.test.jsx` (7 tests) |
| FE-3 | Enter guesses via physical keyboard | `hooks/useKeyboard.js` | `App.test.jsx::handles physical keyboard input` |
| FE-4 | See feedback (green/yellow/gray) | `GameGrid/index.jsx` with status classes | `GameGrid.test.jsx` (5 tests) |
| FE-5 | View guess history | `GameGrid/index.jsx` renders all guesses | `GameGrid.test.jsx::displays guess letters` |
| FE-6 | See when won or lost | `App.jsx` status messages | `App.test.jsx::Win/Lose States` |

---

## Game Rules

| ID | Rule | Implementation | Tests |
|----|------|----------------|-------|
| R-1 | Green = correct position | `LetterStatus.CORRECT` | `test_feedback.py::test_all_correct` |
| R-2 | Yellow = wrong position | `LetterStatus.PRESENT` | `test_feedback.py::test_mixed_feedback` |
| R-3 | Gray = not in word | `LetterStatus.ABSENT` | `test_feedback.py::test_all_absent` |
| R-4 | Answers never plural | `words.py` filters words ending in 's' | `test_words.py::test_returns_non_plural` |
| R-5 | Duplicate letter handling | Two-pass algorithm in `feedback.py` | `test_feedback.py::TestFeedbackDuplicates` (3 tests) |
| R-6 | Must be valid dictionary word | `is_valid_word()` check | `test_api.py::test_submit_invalid_word` |
| R-7 | N+1 guesses for N letters | `Game.max_guesses` property | `test_api.py::test_create_game_*` |
| R-8 | Multiple concurrent games | UUID-based game IDs | Implicitly tested via API tests |

---

## Test Summary

| Component | Test File | Tests |
|-----------|-----------|-------|
| Backend - API | `test_api.py` | 12 |
| Backend - Feedback | `test_feedback.py` | 8 |
| Backend - Words | `test_words.py` | 7 |
| Frontend - App | `App.test.jsx` | 6 |
| Frontend - GameGrid | `GameGrid.test.jsx` | 5 |
| Frontend - Keyboard | `Keyboard.test.jsx` | 7 |
| **Total** | | **45** |

---

## Running Tests

```bash
# Backend (27 tests)
cd backend && PYTHONPATH=. pytest tests/ -v

# Frontend (18 tests)
cd frontend && npm test
```
