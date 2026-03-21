# VIBE-SDD Skills 使用指南

## 概述

VIBE-SDD Skills 遵循 Google Cloud Agent Skills 规范，采用渐进式披露（Progressive Disclosure）模式。

## 三层结构

### L1: 元数据 (始终可见)

```yaml
---
name: skill-name
description: 1-2 句话描述
metadata:
  domain: engineering
  version: "1.0"
  tags: [tag1, tag2]
  examples:
    - "Example 1"
    - "Example 2"
  priority: high
  auto_activate: false
---
```

### L2: 指令 (技能激活时)

```markdown
## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| ... | ✅ Yes |

## L2: How to Use

### Step 1: ...
```

### L3: 资源 (按需加载)

```
references/
├── detailed-guide.md
├── examples.md
└── troubleshooting.md
```

## Skill Registry

所有技能注册在 `skills/registry.yaml`，包含：
- 技能路径
- domain 分类
- priority 优先级
- auto_activate 自动激活标志
- tags 标签
- examples 示例

## A2A Agent Card

`.vic-sdd/agent-card.yaml` 定义了 VIBE-SDD Agent 的完整能力，用于：
- 多 Agent 协作发现
- 能力协商
- 任务委派

## 技能列表

| 技能 | Domain | Priority | Auto Activate |
|------|--------|----------|--------------|
| constitution-check | governance | critical | false |
| context-tracker | engineering | critical | true |
| requirements | product | high | false |
| architecture | engineering | high | false |
| design-review | product | medium | false |
| debugging | engineering | high | false |
| qa | quality | high | false |
| sdd-orchestrator | engineering | critical | false |
| spec-architect | engineering | high | false |
| spec-contract-diff | engineering | high | false |
| spec-traceability | engineering | medium | false |

## 使用流程

1. **Agent 启动** → 读取 Agent Card → 发现可用技能
2. **任务到来** → 查询 Registry → 选择合适技能
3. **技能激活** → 加载 SKILL.md L1+L2 → 执行指令
4. **需要深入** → 加载 references/ → 获取详细信息
5. **任务完成** → 更新 context.yaml → 返回结果
