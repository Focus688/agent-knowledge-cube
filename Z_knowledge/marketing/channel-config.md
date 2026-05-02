# Z: 营销渠道配置

## 渠道矩阵
| 渠道 | 目标 | 预算占比 | 内容类型 | 衡量指标 |
|------|------|---------|---------|---------|
| Google Ads | 需求捕获 | 30% | 着陆页 | CPC, CVR |
| LinkedIn | B2B 触达 | 25% | 白皮书、案例 | CPL, MQL |
| 微信/公众号 | 品牌建设 | 15% | 文章、活动 | 阅读量、互动 |
| 邮件 | 留存 | 10% | Newsletter | 打开率、点击率 |
| SEO | 有机增长 | 20% | 博客、资源页 | 自然流量、排名 |

## UTM 参数规范
`utm_source` — 渠道 (google/linkedin/wechat)
`utm_medium` — 类型 (cpc/social/email)
`utm_campaign` — 活动名称 (q3-launch)

## 追踪设置
- Google Tag Manager 统一管理
- 事件命名: `[category]_[action]_[label]`
- 转化目标: 注册 / Demo预约 / 资料下载
