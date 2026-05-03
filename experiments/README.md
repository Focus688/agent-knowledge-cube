# experiments — 实验场

本目录包含 Agent Knowledge Cube 的实验验证。

## 现有实验

| 实验 | 状态 | 描述 |
|------|------|------|
| `README.md` | ✅ 方案设计 | MVP 验证协议，包含知识边界测试、Token 效率测量、角色冲突检测 |

## 开始实验

```bash
# 1. 加载立方体
python3 -c "
from agent_knowledge_cube import Cube
cube = Cube.load('.')

# 2. 验证知识隔离
eng = cube.get_knowledge_text('software-engineer', 'software-development:implementation')
cs = cube.get_knowledge_text('customer-support-agent', 'customer-service:diagnose')
sales = cube.get_knowledge_text('sales-representative', 'sales-pipeline:close')

# 3. 验证边界
print('工程师知识:', len(eng), 'chars')
print('客服知识:', len(cs), 'chars')
print('销售知识:', len(sales), 'chars')
"
```

## 添加新实验

在 `experiments/` 下创建 `<编号>-<实验名称>/` 目录，内含 `README.md` 说明实验设计、步骤和结果。
