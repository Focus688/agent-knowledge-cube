# Z: Debugging Guide

## Log Levels (in order of verbosity)
- **ERROR**: system is broken, needs human intervention
- **WARN**: something unexpected but non-fatal (retry, fallback)
- **INFO**: major lifecycle events (startup, shutdown, deployment)
- **DEBUG**: detailed flow for development debugging
- **TRACE**: step-by-step execution (only during active debugging)

## Common Error Patterns

| Pattern | Likely Cause | Action |
|---------|-------------|--------|
| 500 | Unhandled exception | Check logs + Sentry |
| 503 | Upstream timeout | Check downstream health |
| 429 | Rate limiting | Check rate limit config |
| Connection pool exhaustion | Too many DB connections | Increase pool, check slow queries |
| OOMKilled | Memory leak | Heap dump analysis |
| CrashLoopBackOff | Config error / startup failure | Check readiness probe + logs |

## Debugging Tools
- **strace**: syscall tracing — `strace -p <PID> -e trace=network`
- **lsof**: open file descriptors — `lsof -i :8080`
- **pprof**: Go CPU/memory profiling — `go tool pprof http://host/debug/pprof/heap`
- **flamegraph**: CPU hotspot visualization (perf + FlameGraph script)
- **curl -v**: full HTTP request/response debugging

## Reproduction Template
```
### Environment: staging/prod/local
### Steps:
1. Call POST /api/orders with payload: {...}
2. Auth header: Bearer <token>
3. Expected: 201 + order object
4. Actual: 500 + "internal error"
### Logs:
[ERROR] order_svc.go:142 — failed to reserve inventory: timeout
```

## Profiling Tips
- Profile under realistic load (not idle)
- Use `pprof` for CPU: sample for 30s under steady request rate
- For goroutine leaks: `pprof goroutine` diff before/after request
- DB: `EXPLAIN ANALYZE` on slow queries, look for seq scans
