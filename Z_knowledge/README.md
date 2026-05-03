# Z_knowledge — 知识库目录

## 用什么做？

知识库是 Agent 的实际知识来源。每个知识文件是 Agent 在特定 (x, y) 坐标下能看到的精确内容。

## 现有知识域

| 域 | 文件数 | 内容类型 |
|----|--------|---------|
| `engineering/` | 22 | 代码规范、技术栈、部署指南、架构文档、安全规范等 |
| `product/` | 9 | PRD模板、用户研究、竞争分析、指标定义、路线图等 |
| `design/` | 4 | 设计系统、视觉指南、素材库、交付标准 |
| `marketing/` | 12 | 策略模板、受众洞察、品牌指南、内容日历、SEO等 |
| `sales/` | 10 | 线索管理、ICP、BANT框架、定价、Demo脚本、合同等 |
| `customer-support/` | 13 | FAQ、工单分流、用户指南、已知问题、知识库管理等 |
| `legal/` | 2 | 合同条款库、合规检查清单 |
| `finance/` | 2 | 发票流程、付款条款 |
| **总计** | **74** | |

## 知识文件规范

- 文件名: 小写 kebab-case，如 `code-standards.md`
- 标题: `# Z: 标题`
- 内容: 简洁、实用、可直接作为 Agent 上下文

## 添加新知识

1. 在对应域下创建 `.md` 文件
2. 在 `_cube_index.yaml` 中引用新文件
3. 在 `Y_workflows/<workflow>.yaml` 中添加 knowledge_slice 引用
