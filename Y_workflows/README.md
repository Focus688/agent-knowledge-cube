# Y_workflows — 工作流目录

## 怎么做？

每个工作流文件定义了完整的流程编排，包含：
- **阶段定义** (stages) — 每个阶段的 id、名称、参与角色
- **知识切片** (knowledge_slice) — 当前阶段需要的知识
- **交接条件** (handoff) — 阶段间的上下文传递
- **验收标准** (verification) — 阶段完成的检查清单

## 现有工作流

| 文件 | 阶段数 | 适用场景 |
|------|--------|---------|
| `software-development.yaml` | 6 | 从需求到部署的完整软件工程流水线 |
| `customer-service.yaml` | 4 | 从问题受理到解决的客服全流程 |
| `marketing-campaign.yaml` | 4 | 从策略制定到效果分析的营销活动 |
| `sales-pipeline.yaml` | 5 | 从线索获取到签约交接的销售全流程 |
| `product-development.yaml` | 5 | 从发现到迭代的产品全生命周期 |

## 添加新工作流

```yaml
name: workflow-name
display: 工作流显示名
description: 描述
stages:
  - id: stage-id
    name: 阶段名称
    roles: [参与角色]
    knowledge_slice: [需要学习的知识文件]
    handoff: 交接说明
    verification: [验收清单]
```

然后在 `_cube_index.yaml` 中添加所有 (role, workflow:stage) → z 的映射。
