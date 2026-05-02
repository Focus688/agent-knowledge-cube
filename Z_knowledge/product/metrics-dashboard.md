# Z: Metrics Dashboard

## 按角色分类 / Key Metrics by Stakeholder

| Stakeholder | Primary Metrics | View |
|-------------|----------------|------|
| **Executive** | Revenue, ARR, NPS, Churn, LTV:CAC | Monthly board report |
| **Product** | Activation, Retention, DAU/MAU, Feature adoption | Weekly squad review |
| **Engineering** | Latency p95, Error rate, Uptime, Build time | Daily operations |
| **Marketing** | CAC, Channel ROI, Conversion rate, MQL-SQL rate | Campaign-level |
| **Support** | CSAT, FRT (First Response Time), Resolution time | Weekly |

## 刷新频率 / Refresh Cadence
- **Real-time**: Error rate, Uptime (PagerDuty/DataDog alerts)
- **Daily**: DAU, Revenue, New signups
- **Weekly**: Retention, Conversion funnel, Feature adoption
- **Monthly**: NPS, Churn, LTV:CAC (board-level)

## 预警阈值 / Alert Thresholds
| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Error rate | >1% | >3% | Page on-call |
| DAU drop | -10% WoW | -20% WoW | Investigate |
| Churn | >5% monthly | >8% monthly | Retention sprint |
| Latency p95 | >500ms | >2s | Eng triage |

## 仪表盘工具 / Dashboard Tools
- **Mixpanel / Amplitude** — product analytics
- **Metabase / Superset** — internal dashboards
- **Mode / Hex** — SQL-driven notebooks + sharing
- **Grafana** — infrastructure + real-time monitoring

## 指标字典 / Metric Dictionary
Maintain a single source of truth in Notion/Coda: definition, SQL query, owner, refresh schedule for every metric.
