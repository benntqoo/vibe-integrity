---
name: vibe-integrity
description: Use when working on a project or need to record/retrieve architecture decisions, risks, and verify code alignment.
---

# Vibe Integrity

统一的 AI 项目记忆与安全系统。

## 快速命令

```bash
# 初始化项目
vic init --name "My Project" --tech "Node.js,Vue,PostgreSQL"

# 记录技术决策
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database" --reason "Need ACID"

# 记录风险
vic rr --id RISK-001 --area auth --desc "JWT handling issue"

# 检查代码对齐
vic check

# 完整验证
vic validate

# 查看状态
vic status
```

## 何时用什么

| 场景 | 命令 |
|------|------|
| 开始新项目 | `vic init` |
| 做了一个技术决策 | `vic rt` |
| 发现一个风险 | `vic rr` |
| AI 说"完成了" | `vic check` |
| 提交前验证 | `vic validate` |
| 备份项目记忆 | `vic export` |

## 相关 Skills

| Skill | 用途 |
|------|------|
| `vibe-think` | 需求澄清、增强提问 |
| `vibe-debug` | 系统性调试方法论 |

## 完整文档

详见 [cmd/vic/README.md](../../cmd/vic/README.md)
