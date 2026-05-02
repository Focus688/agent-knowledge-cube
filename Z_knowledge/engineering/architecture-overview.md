# Z: Architecture Overview (Sales / Public-Facing)

## High-Level Architecture

```
[Customer Apps / Browser]
        ↓ HTTPS (TLS 1.3)
   [CDN + WAF + DDoS Protection]
        ↓
   [Load Balancer] → [API Gateway] → [Microservices] → [DB / Cache / Object Store]
        ↓                        ↓
   [Static Assets]         [Async Workers] → [Message Queue]
```

## Security Posture
- **Encryption**: TLS 1.3 in transit, AES-256 at rest, envelope encryption via KMS
- **Auth**: OAuth 2.0 + OIDC with MFA support; RBAC for fine-grained access
- **Compliance**: SOC 2 Type II certified, GDPR compliant, HIPAA eligible
- **Security**: WAF, DDoS protection, automated vulnerability scanning, SAST/DAST in CI

## Scalability Story
- **Horizontal scaling**: All services are stateless — spin up instances on demand
- **Auto-scaling**: HPA based on CPU/memory/custom metrics (request latency, queue depth)
- **Database**: Read replicas for read scaling, sharding for write scaling
- **Global reach**: Multi-region deployments with active-active or active-passive config
- **Proven throughput**: 10K req/s per API gateway instance, linear scaling with instances

## Compliance Certifications
- SOC 2 Type II (annual audit)
- GDPR (data residency, DPA available)
- HIPAA (BA agreement upon request)
- ISO 27001 (in progress, target Q4 2026)

## Availability
- **SLO**: 99.9% uptime (≈8.7h downtime/year)
- **SLA**: 99.95% for paid plans
- **Multi-AZ deployment** across 3 availability zones
- **Disaster recovery**: RTO <1h, RPO <5min
