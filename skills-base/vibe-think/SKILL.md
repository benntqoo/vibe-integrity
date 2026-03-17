---
name: vibe-think
description: Use when requirements are ambiguous, need to explore options, evaluate trade-offs, or want structured thinking before implementation.
---

# Vibe Think

结构化思考与增强提问工具。

---

## 何时使用

**使用场景：**
- 需求不明确，需要澄清
- 多个方案需要评估权衡
- 技术选型需要分析
- 想要更深入理解问题
- 用户提供模糊描述

**不适用：**
- 需求已清晰
- 正在实现过程中
- 只需要简单确认

---

## 核心方法

### 1. 澄清提问

一次问一个聚焦问题：

```
❌ 不好的提问：
"这个功能需要认证吗？用什么技术栈？数据库选什么？"

✅ 好的提问：
"这个功能涉及敏感数据吗？"
   ↓ (根据回答)
"用户需要登录后才能访问吗？"
   ↓ (根据回答)
"认证方式有偏好吗？JWT 还是 Session？"
```

### 2. 渐进式理解

```
┌─────────────┐
│ 用户描述    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  澄清问题    │ ← 问什么问题？
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  探索选项    │ ← 有哪些方案？
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  权衡分析    │ ← 各有什么优缺点？
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  建议方案    │ ← 推荐哪个？
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  记录决策    │ ← vic record tech
└─────────────┘
```

### 3. 权衡分析模板

```markdown
## 方案对比

| 维度 | 方案 A | 方案 B |
|------|--------|--------|
| 开发成本 | 低 | 高 |
| 维护成本 | 高 | 低 |
| 性能 | 中 | 高 |
| 风险 | 中 | 低 |
| 推荐度 | ⭐⭐⭐ | ⭐⭐⭐⭐ |

**推荐**: 方案 B，因为...
```

---

## 输出

完成后：

1. **理解总结** - 口述或书面
2. **决策记录** - 使用 `vic record tech`
3. **风险识别** - 使用 `vic record risk` (如适用)

```bash
# 记录讨论结果
vic record tech --id ARCH-001 \
  --title "Choose X over Y" \
  --decision "Use X because..." \
  --reason "Trade-off analysis showed..."
```

---

## 示例对话

```
用户: "我想要一个搜索功能"

AI (vibe-think):
"搜索什么内容？用户输入还是结构化查询？"
↓
用户: "用户输入关键词搜索"

AI: "数据量大概多大？几百条还是几百万条？"
↓
用户: "目前几千条，未来可能到百万"

AI: "需要实时搜索还是可以有几秒延迟？"
↓
用户: "实时最好，但1-2秒延迟可以接受"

AI: 
"基于你的需求，我分析两个方案：

| 维度 | SQLite LIKE | Elasticsearch |
|------|-------------|---------------|
| 开发成本 | 低 (1天) | 高 (3-5天) |
| 运维成本 | 无 | 中 |
| 性能 (百万数据) | 差 | 优 |
| 延迟 | <100ms | <50ms |

**推荐**: MVP 阶段用 SQLite LIKE，数据量超过 10 万条时迁移到 Elasticsearch。

要记录这个决策吗？"
↓
用户: "好的"

AI: 
vic record tech --id SEARCH-001 \
  --title "Search Strategy" \
  --decision "SQLite LIKE for MVP, Elasticsearch later" \
  --reason "Data volume currently low, defer infra complexity"
```

---

## 与其他 Skills 的关系

| Skill | 关系 |
|-------|------|
| vic CLI | 记录决策结果 |
| vibe-debug | 分析问题根因 |
| vibe-integrity | 读取项目上下文 |

---

## 快速检查清单

澄清前问自己：
- [ ] 我理解核心问题了吗？
- [ ] 有哪些约束条件？
- [ ] 有哪些方案可选？
- [ ] 各方案的权衡是什么？
- [ ] 我的建议基于什么理由？
