# Z: Post-Deployment Smoke Test Checklist

Run immediately after every deployment before marking it complete.

## Critical User Journeys
- [ ] Public landing page loads (200, no console errors)
- [ ] User registration → login flow works end-to-end
- [ ] Search returns results (empty query + valid query)
- [ ] Core CRUD: create, read, update, delete a resource
- [ ] File upload/download (if applicable) — correct MIME + size limit

## API Health
- [ ] Health endpoint: `GET /health` returns 200 with readiness
- [ ] Metrics endpoint: `GET /metrics` returns Prometheus output
- [ ] Auth endpoints: login (200), invalid credentials (401), expired token (401)
- [ ] Rate-limited endpoint returns 429 under load
- [ ] Pagination works (page 1, page 2, beyond last page → empty)

## Database
- [ ] Schema migration applied (check latest migration version)
- [ ] Read replicas are in sync (no replication lag spikes)
- [ ] Redis cache is warmable / prime command works

## Infrastructure
- [ ] All pods/nodes are healthy (`kubectl get pods --all-namespaces`)
- [ ] TLS certificate valid (no expiry warnings)
- [ ] Logs are flowing to Loki/Grafana
- [ ] Alerts are not firing for the new deployment

## Dependencies
- [ ] Downstream APIs respond correctly (check external integrations)
- [ ] Webhook callbacks reachable
- [ ] Queues: consumers connected, message count stable
