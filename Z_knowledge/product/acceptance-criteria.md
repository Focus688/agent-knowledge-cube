# Z: Acceptance Criteria Writing Guide

## Given-When-Then 格式 / Format

```
Scenario: [Title]
  Given [initial context / precondition]
  When [action / trigger occurs]
  Then [expected outcome / observable result]
```

### Example
```
Scenario: User resets password
  Given the user is on the login page
  When they click "Forgot Password" and enter their email
  Then a password reset link is sent to that email
  And the user sees a confirmation message
```

## 边界条件 / Edge Cases
- Empty states (no data, first-time user)
- Maximum input length / volume
- Network failure, timeout, retry behavior
- Concurrent access / race conditions
- Special characters, XSS injection handling

## 负面场景 / Negative Scenarios
- Invalid input → proper error messages
- Unauthorized access → redirect or 403
- Expired sessions → graceful re-auth prompt
- Rate limiting → user-friendly cooldown

## Definition of Done (DoD) Checklist
- [ ] Code reviewed and merged
- [ ] Unit tests pass (coverage ≥80%)
- [ ] Integration / E2E tests pass
- [ ] Acceptance criteria verified by QA
- [ ] Accessibility (WCAG AA) checked
- [ ] Localization strings extracted
- [ ] Documentation updated
- [ ] Analytics events implemented
- [ ] No P0/P1 bugs open
- [ ] Product owner signed off

## 关键词 / Keywords
- **And, But** — chain conditions
- **@smoke, @regression** — test tagging
