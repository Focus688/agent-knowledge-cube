# Z: Performance Benchmarks & Data

## API Latency Targets (internal services)
| Percentile | Target | Warning | Critical |
|-----------|--------|---------|----------|
| P50  | <50ms  | 100ms   | 200ms    |
| P95  | <200ms | 500ms   | 1s       |
| P99  | <500ms | 1s      | 2s       |

## Throughput Baselines
- **API Gateway**: 10K req/s per instance (2 vCPU, 4GB RAM)
- **Web server**: 5K req/s per instance
- **Worker (async)**: 1K messages/s per consumer
- **Single instance limits** scale linearly with CPU up to 8 vCPU

## Resource Utilization Norms
| Resource | Target | Alert |
|----------|--------|-------|
| CPU      | <60%  avg | >80% for 5min |
| Memory   | <70%  avg | >85% for 5min |
| Disk I/O | <50%  max | >80% sustained |
| Network  | <40%  link capacity | >70% sustained |

## Database Query Performance
- **Simple CRUD** (by PK): <5ms P50, <20ms P99
- **List with filter + sort + pagination**: <50ms P95 (with proper index)
- **Joins (3 tables)**: <100ms P95 (with covering index)
- **Full-text search**: <200ms P95 (with GIN index)
- **Danger zone**: queries >1s — must be optimized or cached

## Caching Strategy
- **Redis**: <1ms read, <5ms write (in-memory)
- **CDN**: edge cache TTL 1h for static assets, 5min for API responses
- **Local cache**: in-process LRU (max 100MB), TTL 30s
- Cache hit ratio target: >80% for read-heavy endpoints
