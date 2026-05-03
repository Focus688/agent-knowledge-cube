# X_roles — 角色目录

## 谁做？

每个角色文件定义了：
- **角色职责** (description)
- **技能清单** (skills)
- **行为约束** (cannot / must_follow)
- **知识边界** (must_know / optional / forbidden)

## 角色分类

| 分类 | 角色 | 数量 |
|------|------|------|
| `engineering/` | software-engineer, devops-engineer, qa-engineer, data-engineer, security-engineer | 5 |
| `product/` | product-manager, product-designer, data-analyst | 3 |
| `design/` | ui-designer, ux-researcher | 2 |
| `marketing/` | marketing-specialist, content-creator | 2 |
| `sales/` | sales-representative | 1 |
| `customer-support/` | customer-support-agent, technical-support-engineer | 2 |
| `management/` | engineering-manager, project-manager | 2 |
| `operations/` | hr-specialist, legal-counsel, finance-specialist | 3 |

## 添加新角色

```yaml
# X_roles/<category>/<role-name>.yaml
name: role-name
display: 角色显示名
category: 分类
description: 一句话职责描述
skills: [技能1, 技能2]
constraints:
  cannot: [不能做的事]
  must_follow: [必须遵守的流程]
knowledge_boundary:
  must_know: [必须知道的知识]
  optional: [可选知识]
  forbidden: [禁止访问的知识]
```

然后在 `_cube_index.yaml` 中添加对应的 (x, y) → z 映射。
