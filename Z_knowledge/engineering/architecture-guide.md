# Z: Architecture Guide — System Overview

## Topology
```
[Client] → CDN → [Load Balancer] → [API Gateway] → [Microservices] → [DB/Queue/Cache]
                                                      ↕
                                              [Message Queue]
```

## Components
- **Frontend**: React/Next.js SPA, SSG for docs, PWA support
- **Backend**: Go/Rust microservices (or Python/FastAPI for rapid iteration)
- **API Layer**: REST + gRPC, GraphQL for complex queries
- **Database**: PostgreSQL (primary), Redis (cache), Elasticsearch (search)
- **Queue**: RabbitMQ / Kafka for async processing

## Architecture Principles
- **Loose Coupling**: Services communicate via APIs/events, never direct DB access
- **Single Responsibility**: Each service owns one domain (auth, billing, search...)
- **Stateless**: Every instance is disposable — all state lives in DB/cache
- **Fail Fast**: Validate inputs at the boundary; reject invalid requests early
- **Observability**: Every service emits metrics, logs, traces by default

## Deployment
- Kubernetes (EKS/GKE/AKS) with Helm charts
- Multi-AZ for HA, pod disruption budgets for rolling updates
- Blue-green deployments for zero-downtime releases
