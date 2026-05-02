# Z: Hotfix and Patch Guide

## Severity Classification
- **Critical (P0)**: Service down, data loss, security breach — fix within 1h
- **High (P1)**: Major feature broken affecting >10% users — fix within 4h
- **Medium (P2)**: Minor bug, no user-facing impact — next release cycle
- **Low (P3)**: Cosmetic, nice-to-have — backlog

## Expedited Review Process
- Skip full CI if tests are unrelated (document the skip reason)
- At least one senior engineer must approve the hotfix PR
- Review focuses on: "Does this fix the issue? Does it break anything else?"
- Automated security scan still runs (cannot skip)

## Minimal Change Principle
- Change **only** the code that fixes the bug — no refactoring
- No style changes, no unrelated imports, no formatting drift
- If a refactor is needed, create a separate follow-up ticket
- Prefer a 1-line fix over a 50-line restructure

## Testing Requirements for Patches
- Hotfix must include a test that reproduces the bug (fails before, passes after)
- If adding the test is impractical, document why and manual test steps
- Run the full test suite for the affected module (at minimum)
- Deployment: canary first, observe for 10min before full rollout
- Rollback plan ready before deployment starts

## Documentation
- Tag hotfix PR with `hotfix` label in GitHub
- Link hotfix to the incident ticket
- Post-mortem must explain why the bug wasn't caught by existing tests
