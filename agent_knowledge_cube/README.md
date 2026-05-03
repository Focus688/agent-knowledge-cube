# agent_knowledge_cube — Python 库

## 安装

```bash
cd /path/to/agent-knowledge-cube
pip install -e .
```

## CLI 用法

```bash
# 列出所有角色
cube list roles

# 获取工程师在开发阶段的知识
cube knowledge software-engineer software-development:implementation

# 获取客服 Agent 在服务流程中的完整上下文
cube agent customer-support-agent customer-service

# 权重优化（新思路）
cube optimize "紧急修复生产故障" --top-k 3

# 对比 heuristic 和 LLM 两种权重模式
cube compare "客户投诉响应慢"

# 查看立方体统计
cube stats
```

## Python API

```python
from agent_knowledge_cube import Cube, WeightedOptimizer

# 思路一：硬查表
cube = Cube.load('.')
text = cube.get_knowledge_text('software-engineer', 'software-development:implementation')

# 思路二：权重调参
optimizer = WeightedOptimizer(cube)
results = optimizer.optimize('需要优化客服流程', top_k=3)
```

## 架构

```
agent_knowledge_cube/
├── __init__.py      # 入口
├── loader.py        # Cube 核心：加载索引、查询知识
├── optimizer.py     # WeightedOptimizer：权重评分 + LLM 调参
└── cli.py           # 命令行接口
```
