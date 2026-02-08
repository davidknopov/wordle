# Future Improvements

What I'd add for production, with rationale for what was intentionally deferred.

---

## Intentionally Deferred (Assessment Scope)

These were conscious decisions, not oversights:

| Item | Why Deferred | Production Approach |
|------|--------------|---------------------|
| **TypeScript** | Starter was JavaScript; converting mid-assessment adds risk without functional benefit | Use TS from project start, or migrate incrementally |
| **E2E Tests** | Unit + integration tests cover correctness; E2E is operational confidence | Playwright for critical paths: start game → win, start → lose |
| **Environment Config** | Single deployment target (localhost) | `VITE_API_URL` env var, `.env.example` file |
| **Authentication** | Anonymous games sufficient for demo | JWT or session-based auth, user accounts |
| **Database Persistence** | In-memory with Repository abstraction allows easy swap | Redis (with TTL) → PostgreSQL (for analytics) |
| **Rate Limiting** | No abuse vector in assessment context | Backend middleware: 10 guesses/min per IP |
| **Logging/Monitoring** | Local development only | Structured logging, Sentry for errors, basic metrics |
| **CI/CD Pipeline** | Manual testing sufficient for submission | GitHub Actions: lint → test → build → deploy |

---

## High Priority (Would Do Next)

### 1. Input Validation UX
- **Current**: Error message after invalid submit
- **Better**: Shake animation, prevent submit until word complete
- **Effort**: 2 hours

### 2. Tile Flip Animation
- **Current**: Colors appear instantly
- **Better**: Sequential tile flip revealing colors
- **Effort**: 3 hours

### 3. localStorage Persistence
- **Current**: Refresh loses game
- **Better**: Store gameId, restore on load
- **Effort**: 1 hour

### 4. Share Results
- **Current**: No sharing
- **Better**: Copy emoji grid (⬛🟨🟩) to clipboard
- **Effort**: 1 hour

---

## Medium Priority (Polish)

| Feature | Description | Effort |
|---------|-------------|--------|
| Hard Mode | Must reuse confirmed letters | 2 hours |
| Statistics | Win %, guess distribution, streak | 3 hours |
| Dark/Light Toggle | System preference + manual override | 1 hour |
| Accessibility | ARIA labels, screen reader support, focus management | 4 hours |

---

## Lower Priority (Nice-to-Have)

- Sound effects (toggleable)
- Confetti on win
- Hint system (reveal one letter)
- Daily challenge mode
- Multiplayer race mode
- Word definitions after game

---

## Technical Debt

| Item | Status | Notes |
|------|--------|-------|
| Unit tests (feedback algorithm) | ✅ Done | 11 tests, covers duplicates |
| API integration tests | ✅ Done | 12 tests, covers error cases |
| Frontend component tests | ✅ Done | 18 tests |
| E2E tests | ⬜ Deferred | Would add for production |
| Error boundaries | ⬜ Deferred | React error boundary for graceful failures |
| API retry logic | ⬜ Deferred | Exponential backoff for network failures |

---

## Production Deployment

If deploying this for real users:

```
Backend:
  - AWS Lambda + API Gateway (serverless, scales to zero)
  - Or ECS Fargate (if need persistent connections)
  - Redis ElastiCache for game state (with 24h TTL)
  - CloudWatch for logs/metrics

Frontend:
  - S3 + CloudFront (static hosting)
  - Environment-specific builds (staging, prod)

Infrastructure:
  - Terraform or CDK for IaC
  - GitHub Actions for CI/CD
  - Route53 for DNS
```

---

## Summary

The current implementation prioritizes:
1. **Correctness** - Algorithm handles all edge cases
2. **Code Quality** - Clean architecture, consistent patterns
3. **Testability** - 45 tests, good coverage
4. **Documentation** - Tradeoffs explained, decisions justified

What's deferred is documented, not forgotten.
