# Future Improvements & Nice-to-Haves

Things I'd add with more time, roughly prioritized by impact.

---

## High Priority (Would Do Next)

### 1. Input Validation UX
- **Current**: Error message appears after submit
- **Better**: Prevent submission until word is complete, shake animation on invalid word
- **Why**: Reduces friction, matches real Wordle behavior

### 2. Tile Flip Animation
- **Current**: Colors appear instantly
- **Better**: Tiles flip one-by-one revealing colors (like real Wordle)
- **Why**: Builds suspense, more satisfying UX

### 3. Game Persistence (localStorage)
- **Current**: Refresh = lose current game
- **Better**: Store `gameId` in localStorage, restore on page load
- **Why**: Prevents accidental loss of in-progress games

### 4. Loading States
- **Current**: No feedback during API calls
- **Better**: Disable keyboard during submission, show spinner
- **Why**: Prevents double-submission, clearer feedback

---

## Medium Priority (Polish)

### 5. Hard Mode
- **What**: Must use confirmed green/yellow letters in subsequent guesses
- **Implementation**: Validate guess against known constraints before API call
- **Why**: Adds challenge for experienced players

### 6. Statistics Tracking
- **What**: Games played, win %, guess distribution, streak
- **Implementation**: localStorage for anonymous stats, or user accounts for persistence
- **Why**: Engagement, sense of progression

### 7. Share Results
- **What**: Copy emoji grid to clipboard (⬛🟨🟩 format)
- **Implementation**: Generate emoji string from guess history
- **Why**: Social/viral feature, core to Wordle's success

### 8. Keyboard Letter Status Persistence
- **Current**: Keyboard colors reset on new game
- **Better**: Already works correctly, but could animate color changes
- **Why**: Visual polish

### 9. Dark/Light Mode Toggle
- **Current**: Dark mode only
- **Better**: System preference detection + manual toggle
- **Why**: Accessibility, user preference

---

## Lower Priority (Nice-to-Have)

### 10. Sound Effects
- Key press clicks, win/lose sounds
- Should be toggleable

### 11. Confetti on Win
- Celebration animation
- Libraries: canvas-confetti

### 12. Hint System
- Reveal one letter (costs a guess or limited uses)
- Good for accessibility/casual players

### 13. Daily Challenge Mode
- Same word for everyone each day
- Requires: scheduled word selection, prevent replay

### 14. Multiplayer
- Race mode: same word, first to solve wins
- Requires: WebSocket, matchmaking, shared game state

### 15. Word Definitions
- Show definition of target word after game ends
- API: Free Dictionary API
- Educational value

---

## Technical Debt

### 16. Tests
- ✅ Unit tests for feedback algorithm (11 tests)
- ✅ API integration tests (13 tests)
- ✅ Word validation tests (10 tests)
- ✅ Frontend component tests (18 tests)
- ⬜ E2E tests for full game flow (Playwright)

### 17. Error Boundaries
- React error boundary to catch rendering errors
- Graceful fallback UI

### 18. API Retry Logic
- Retry failed requests with exponential backoff
- Better offline handling

### 19. Rate Limiting
- Backend: Prevent brute-force guessing
- Frontend: Debounce rapid submissions

### 20. Logging & Monitoring
- Structured logging
- Error tracking (Sentry)
- Basic analytics

---

## Infrastructure

### 21. Docker Compose for Full Stack
- **Current**: Backend only in Docker
- **Better**: Both services in compose with proper networking

### 22. Production Deployment
- Backend: AWS Lambda or ECS
- Frontend: S3 + CloudFront
- Database: DynamoDB or RDS

### 23. CI/CD Pipeline
- Lint, test, build on PR
- Auto-deploy on merge to main

---

## What I Intentionally Skipped

| Feature | Reason |
|---------|--------|
| User authentication | Out of scope for assessment |
| Database persistence | In-memory sufficient for demo |
| Comprehensive tests | Time constraint, focused on functionality |
| Animations | Prioritized correctness over polish |
| PWA/offline support | Would need service worker, caching strategy |

---

## If I Had 2 More Hours

1. Tile flip animations
2. localStorage game persistence  
3. Share results feature
4. Unit tests for feedback algorithm

These four would significantly improve the feel of the app while demonstrating attention to detail.
