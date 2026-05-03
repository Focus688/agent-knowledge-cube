# Contributing to Agent Knowledge Cube

感谢你愿意参与这个项目！无论是补全角色目录、完善知识库，还是提建议，都欢迎。

## 贡献方式

### 🐛 报告问题
- 在 [Issues](https://github.com/Focus688/agent-knowledge-cube/issues) 提交
- 标明是 Bug / 新需求 / 讨论
- 提供复现步骤（如果是 Bug）

### 📚 补全角色 / 工作流 / 知识

1. Fork 本仓库
2. 添加或修改文件：
   - **角色**: `X_roles/<category>/<name>.yaml`
   - **工作流**: `Y_workflows/<name>.yaml`
   - **知识**: `Z_knowledge/<domain>/<name>.md`
3. 更新 `_cube_index.yaml` 添加对应的 (x, y) → z 映射
4. 提交 PR

### 💡 提想法

在 [Discussions](https://github.com/Focus688/agent-knowledge-cube/discussions) 开帖：
- **新行业**：你希望看到哪个行业的 XYZ 目录？
- **新思路**：对权重模型、协调算法的改进想法
- **使用案例**：你在项目中是怎么用 Cube 的？

## 开发规范

### 代码风格
- Python: PEP 8, type hints
- YAML: 2 空格缩进
- Markdown: 中文 + 英文混排，保持简洁

### 知识文件规范
- 文件名: `kebab-case.md`
- 标题: `# Z: 标题`
- 内容: 300-1000 字，聚焦实用参考，不写废话

### 提交信息格式
```
<type>: <简短描述>

feat:    新角色/工作流/知识文件
fix:     修复错误
docs:    文档
refactor:重构
```

## PR 流程
1. 创建 feature branch
2. 提交改动
3. 确保 `cube stats` 命令正常输出
4. 提交 PR，描述改动内容和目的

---

任何问题，直接在 [Discussions](https://github.com/Focus688/agent-knowledge-cube/discussions) 问。
