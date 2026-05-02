# Z: Rollback Plan

## Rollback Types

### Canary Rollback
- Stop routing traffic to canary instances
- Scale down canary, restore original deployment
- Monitor for 5min to confirm recovery

### Full Rollback
1. `kubectl rollout undo deployment/<svc> --to-revision=<N>`
2. Or redeploy previous CI artifact (Docker image tag `vX.Y.Z`)
3. Verify health check passes
4. Gradually shift traffic (10% → 50% → 100%)

### Database Migration Rollback
- **Forward migration only** — every migration must have a `down.sql`
- Run: `migrate -path migrations -database $DB_URL down N`
- Verify schema state matches the application version
- Data backfill migrations: ensure reverse backfill exists

### Feature Flag Toggle
- Kill switch: disable feature flag → behavior reverts to old code path
- Flags must be evaluated at runtime, not compile time
- TTL cache on flag state: max 60s propagation delay

## Verification Steps
- [ ] Health check endpoint returns 200
- [ ] Key user flow works (login, read, write)
- [ ] Error rate returns to baseline (within 10min)
- [ ] Database migration is in correct direction
- [ ] Alert rules silence temporary noise

## Communication Protocol
1. **Declare rollback** in #incident Slack channel with `/rollback`
2. Notify stakeholders: "Reverting deployment vX.Y.Z due to {reason}"
3. After rollback: verify + post in #incident with all-clear
4. Schedule post-mortem within 24h
