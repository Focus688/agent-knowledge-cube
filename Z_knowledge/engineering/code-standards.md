# Z: 代码规范
# 知识域 — 工程类

## 命名规范
- **类名**: PascalCase
- **函数/方法**: snake_case
- **常量**: UPPER_SNAKE_CASE
- **私有成员**: _prefix
- **文件命名**: snake_case.py / kebab-case.ts

## Git 提交规范
```
<type>(<scope>): <description>

feat:    新功能
fix:     修复
refactor:重构
docs:    文档
test:    测试
chore:   构建/工具
perf:    性能
```

## 代码审查 Checklist

### 功能完整性
- [ ] 需求覆盖所有验收条件
- [ ] 边界情况已处理（空值、边界值、异常输入）
- [ ] 错误处理完善

### 代码质量
- [ ] 无重复代码（DRY）
- [ ] 函数职责单一
- [ ] 复杂度合理（循环复杂度 < 10）
- [ ] 命名自解释

### 安全
- [ ] 用户输入已校验/转义
- [ ] 无硬编码凭据
- [ ] SQL 注入防护
- [ ] XSS 防护

### 性能
- [ ] N+1 查询检查
- [ ] 缓存策略适当
- [ ] 大数据集分页处理
