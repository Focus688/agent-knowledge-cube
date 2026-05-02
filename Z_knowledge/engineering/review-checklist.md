# Z: Code Review Checklist

## Functional Correctness
- [ ] Does the code satisfy all acceptance criteria?
- [ ] Are edge cases handled (empty, null, max values)?
- [ ] Are error paths properly handled, not just happy paths?
- [ ] Are all state transitions valid?
- [ ] Concurrency safety — any race conditions?

## Code Quality
- [ ] Follows project style guide (lint passes)
- [ ] No dead code, commented blocks, or TODOs without tickets
- [ ] Functions/methods are small and single-purpose
- [ ] Naming is clear and consistent (no abbreviations)
- [ ] DRY — duplicate logic extracted
- [ ] Logging at appropriate levels (not verbose in hot paths)

## Security
- [ ] SQL injection: use parameterized queries, not string interpolation
- [ ] XSS/CSRF protection in place
- [ ] Secrets (keys, passwords) not hardcoded
- [ ] Authentication tokens validated and revoked properly
- [ ] Input validation on all external data

## Performance
- [ ] No N+1 queries — batch loading used
- [ ] Database queries have proper indexes
- [ ] Caching strategy applied where appropriate
- [ ] No synchronous blocking calls in async paths
- [ ] Memory usage reasonable (no large allocations in loops)

## Testing Coverage
- [ ] Unit tests for core logic
- [ ] Integration tests for API endpoints
- [ ] Tests for error paths and edge cases
- [ ] Test data is isolated and repeatable

## Documentation
- [ ] Public API has docstrings/OpenAPI annotations
- [ ] README or comment explains non-obvious design decisions
- [ ] Migration/changelog entry created if needed
