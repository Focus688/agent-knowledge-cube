# Z: Emergency Hotfix Procedure

## Severity Definitions
- **S0 (Critical)**: Production unavailable, active data loss, security breach in progress
- **S1 (High)**: Major feature broken for >50% of users, degraded but not down

## Freeze Exception
- Hotfixes bypass the regular deployment freeze window
- Exception requires VP/Director approval (documented in Slack)
- Only the hotfix change is deployed — no other queued changes

## Expedited Deployment
1. **Branch**: Create from `main` at the last known-good commit
2. **Fix**: Apply the minimal change (see patch-guide.md)
3. **Review**: Senior engineer reviews within 15min (async OK, no meeting)
4. **CI**: Run tests for affected module only (full CI if it completes in <10min)
5. **Deploy**: Directly to production — skip staging if needed
6. **Monitor**: Watch error rate, latency, and traffic for 30min

## Communication Protocol
- **Declare**: `:rotating_light: S0/S1 incident declared — hotfix deploying`
- **Status updates**: Every 15min in #incident channel
- **Resolved**: Post with all-clear, link to PR, link to runbook
- **Notify**: On-call engineer, engineering manager, product owner

## Post-Mortem Requirements
- Timeline: detection → response → fix → recovery
- Root cause analysis (5 Whys)
- Why wasn't this caught by existing tests/monitoring?
- Action items: test gap, monitoring gap, process gap
- Post-mortem completed within 24h (48h max for S1)
