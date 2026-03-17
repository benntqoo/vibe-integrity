---
name: vibe-debug
description: Use when encountering bugs, test failures, or unexpected behavior and need systematic root cause analysis before proposing fixes.
---

# Vibe Debug

系统性调试方法论。

---

## 何时使用

**使用场景：**
- 测试失败
- Bug 需要修复
- 意外行为
- 错误信息不清楚

- 尝试修复但问题仍然存在

**不适用：**
- 语法错误（直接修复)
- 简单配置问题
- 明确的问题

- 正在编写新代码

---

## 核心原则

> **Never fix a symptom without understanding the root cause.**

---

## 四阶段流程

### Phase 1: 根因调查

**必须完成：**

1. **仔细阅读错误信息**
   - 不跳过错误/警告
   - 完整阅读堆栈跟踪
   - 检查 vic check 输出

2. **可靠复现**
   - 能稳定触发吗？
   - 步骤是什么？
   - 每次都一样吗？

3. **检查最近变更**
   ```bash
   git diff --name-only HEAD~5
   ```

4. **多组件诊断**
   - 每个边界加日志
   - 检查状态传递
   - 定位失败点

### Phase 2: 模式分析

- 找到工作的示例
- 对比实现差异
- 检查依赖关系

### Phase 3: 假设测试

- **一次一个假设**
- 最小化测试
- 验证后继续

### Phase 4: 实现
- 创建失败测试
- **单一修复**
- 验证修复

- **如果 3+ 次失败 → 质疑架构**

---

## 红旗信号

立即返回 Phase 1：

- "快速修复"
- "试试改 X 看看"
- "多个改动一起测"
- "跳过测试，- "应该没问题"
- "3+ 次失败"
- "一边修一边加"

---

## 调试完成后

```bash
# 讣录发现的洞察
vic record risk --id RISK-XXX --area "..." --desc "..."
```
