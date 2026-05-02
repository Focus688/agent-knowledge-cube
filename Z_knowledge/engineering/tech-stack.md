# Z: 技术栈文档
# 知识域 — 工程类

## 后端
- **语言**: Python 3.11+
- **框架**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **消息队列**: RabbitMQ

## 前端
- **语言**: TypeScript 5.x
- **框架**: React 18 + Next.js 14
- **状态管理**: Zustand
- **样式**: Tailwind CSS
- **包管理器**: pnpm

## 基础设施
- **容器**: Docker + Docker Compose
- **编排**: Kubernetes (生产)
- **CI/CD**: GitHub Actions
- **监控**: Prometheus + Grafana
- **日志**: Loki + Grafana
- **APM**: OpenTelemetry

## API 设计原则
- RESTful 风格
- 版本控制: URL 路径 (v1, v2)
- 响应格式统一
- 认证: JWT Bearer Token
- 限流: 100 req/min per user
