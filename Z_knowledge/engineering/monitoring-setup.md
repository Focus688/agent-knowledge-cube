# Z: Monitoring Setup

## Metrics (Prometheus)
- RED metrics: Rate, Errors, Duration for every service endpoint
- USE metrics: Utilization, Saturation, Errors for infrastructure
- Custom business metrics: signups/sec, orders/min, revenue/hour
- Exporters: node_exporter, postgres_exporter, redis_exporter

## Dashboards (Grafana)
- **Service Dashboard**: per-service latency, error rate, request rate, CPU/mem
- **Business Dashboard**: DAU, MAU, conversion funnel, revenue
- **Infra Dashboard**: cluster health, node status, pod restarts, disk usage
- **Alerting Dashboard**: active alerts, silenced rules, notification history

## Alert Rules
- P0 (critical): service down, error rate >5%, p99 latency >2s
- P1 (warning): error rate >1% for 5min, CPU >80%, disk >85%
- P2 (info): deployment completed, cert expires in 30d
- Use Alertmanager with routing: P0→PagerDuty, P1→Slack, P2→email

## SLI / SLO Definitions
- **Availability SLI**: % of requests returning 2xx/3xx/4xx (not 5xx)
- **Latency SLI**: p99 latency over 5min window
- **Throughput SLI**: requests/sec per service
- **SLO target**: 99.9% availability, p99 <500ms, p95 <200ms

## Log Aggregation
- Structured JSON logging only (no freeform text)
- Loki for log aggregation, query via LogQL
- Correlation ID (trace_id) in every log line
- 30-day retention for logs; 90-day for cold storage

## APM Tracing
- OpenTelemetry SDK auto-instrumentation
- Trace every external call (DB, queue, HTTP, gRPC)
- Sample rate: 100% for critical paths, 1% for high-throughput
