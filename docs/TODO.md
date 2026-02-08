# Future Improvements

What I'd add for production, and what was intentionally scoped out.

---

## Intentionally Deferred

| Item | Rationale |
|------|-----------|
| **TypeScript** | Starter was JavaScript; converting adds risk without functional benefit for assessment |
| **E2E Tests** | Unit + integration cover correctness; E2E is for operational confidence in production |
| **Environment Config** | Single target (localhost); production would use env vars |
| **Authentication** | Anonymous games sufficient for demo |
| **Database** | In-memory with Repository pattern allows easy swap to Redis/Postgres |
| **Rate Limiting** | No abuse vector in assessment; would add for production |
| **CI/CD** | Manual testing sufficient; would add GitHub Actions for production |

---

## Production Additions

**UX Polish**
- Tile flip animations
- Shake on invalid word
- localStorage game persistence
- Share results (emoji grid)

**Features**
- Hard mode (must reuse confirmed letters)
- Statistics tracking
- Dark/light mode toggle

**Infrastructure**
- Backend: Lambda + API Gateway or ECS
- Frontend: S3 + CloudFront
- State: Redis with TTL
- Monitoring: CloudWatch, Sentry

**Quality**
- E2E tests (Playwright)
- Error boundaries
- Accessibility (ARIA, focus management)

---

## Summary

Current implementation prioritizes correctness, clean architecture, and test coverage. Production concerns are documented, not forgotten.
