# VIBE-SDD Skills 系统改善计划

> **生成时间**: 2026-03-21
> **状态**: 待执行
> **目标**: 将 VIBE-SDD Skills 系统对齐 Google Cloud Agent Skills 规范

---

## 问题诊断

基于 Google Cloud Agent Skills 规范对比分析：

| 问题 | 严重度 | 说明 |
|------|--------|------|
| 无 Progressive Disclosure (L1/L2/L3) | 🔴 高 | 所有内容一次性加载，token 浪费 |
| 无 Agent Card | 🔴 高 | 无法被其他 Agent 发现 |
| 无 references/ 子目录 | 🔴 高 | 详细文档膨胀核心文件 |
| 无 Skill Registry | 🟡 中 | 无法自动发现可用技能 |
| 无 metadata 扩展 | 🟡 中 | 缺少 version/tags/examples |
| 无 assets/scripts 目录 | 🟢 低 | 缺少模板和脚本支持 |

---

## 改善方案

### 核心理念：渐进式披露（Progressive Disclosure）

```
L1 (元数据) ──────► name + description + tags + examples   [始终可见]
                     ↓
L2 (指令) ─────────► When to Use + How to Use              [技能激活时]
                     ↓
L3 (资源) ─────────► references/ + assets/ + scripts/       [按需加载]
```

---

## 实施阶段

### 阶段 1：建立目录结构标准（P0）

#### 1.1 定义标准目录结构模板

**创建文件**: `skills/_template/SKILL.md`

```markdown
---
name: template-skill
description: [1-2 句话描述技能作用，AI 用于决策是否激活]
metadata:
  domain: [engineering|product|quality|governance]
  version: "1.0"
  tags: [tag1, tag2, tag3]
  examples:
    - "Example 1: when to use this skill"
    - "Example 2: another scenario"
  priority: [critical|high|medium|low]
  auto_activate: [true|false]
---

# [Skill Name]

## Overview

[1-3 句话描述技能的核心价值]

## L1: When to Use (触发条件)

[精简的触发条件列表，AI 用于快速判断]
[格式: 场景 → 使用此技能]

## L2: How to Use (使用流程)

### Step 1: [具体步骤]
[详细说明]

### Step 2: [具体步骤]
[详细说明]

[参考: references/step-by-step.md]

## L3: References (按需加载)

- references/
  - `detailed-guide.md` - 完整使用指南
  - `examples.md` - 更多示例
  - `troubleshooting.md` - 故障排除
- assets/
  - `template.md` - 输出模板
- scripts/
  - `setup.sh` - 初始化脚本
```

#### 1.2 创建 Skill Registry

**创建文件**: `skills/registry.yaml`

```yaml
# VIBE-SDD Skill Registry
# ========================
# 定义所有可用技能及其元数据
# 用于 Agent 发现和技能路由

version: "1.0"
updated: "2026-03-21"

skills:
  - name: constitution-check
    path: ./constitution-check/SKILL.md
    domain: governance
    priority: critical
    auto_activate: false
    description: "Verifies rules compliance before plans, reviews, commits"
    tags: [compliance, governance, blocking]
    examples:
      - "Before generating implementation plans"
      - "Before git commits"

  - name: context-tracker
    path: ./context-tracker/SKILL.md
    domain: engineering
    priority: critical
    auto_activate: true
    description: "Tracks AI knowledge state and confidence at every moment"
    tags: [self-awareness, monitoring, confidence]
    examples:
      - "At task BEGIN"
      - "After every meaningful action"

  - name: requirements
    path: ./requirements/SKILL.md
    domain: product
    priority: high
    auto_activate: false
    description: "Clarifies vague requirements into structured user stories"
    tags: [requirements, clarification, user-stories]
    examples:
      - "User requirements are ambiguous"
      - "Need to define acceptance criteria"

  - name: architecture
    path: ./architecture/SKILL.md
    domain: engineering
    priority: high
    auto_activate: false
    description: "Makes technology stack decisions and system architecture design"
    tags: [architecture, tech-stack, design]
    examples:
      - "Need to select technology stack"
      - "Design system architecture"

  - name: design-review
    path: ./design-review/SKILL.md
    domain: product
    priority: medium
    auto_activate: false
    description: "Reviews UI/UX designs for quality and consistency"
    tags: [design, ui, ux, review]
    examples:
      - "Build UI design system"
      - "Review design mockups"

  - name: debugging
    path: ./debugging/SKILL.md
    domain: engineering
    priority: high
    auto_activate: false
    description: "Systematic 4-phase root cause analysis methodology"
    tags: [debugging, root-cause, quality]
    examples:
      - "Bug fix"
      - "Test failure investigation"

  - name: qa
    path: ./qa/SKILL.md
    domain: quality
    priority: high
    auto_activate: false
    description: "Test-driven development and test coverage enforcement"
    tags: [testing, tdd, quality, coverage]
    examples:
      - "Write tests for new feature"
      - "Check test coverage"

  - name: sdd-orchestrator
    path: ./sdd-orchestrator/SKILL.md
    domain: engineering
    priority: critical
    auto_activate: false
    description: "Manages SDD workflow state machine and pipeline transitions"
    tags: [orchestration, sdd, pipeline, workflow]
    examples:
      - "Manage SDD workflow"
      - "State transition between phases"

  - name: spec-architect
    path: ./spec-architect/SKILL.md
    domain: engineering
    priority: high
    auto_activate: false
    description: "Builds executable specs from ambiguous requirements"
    tags: [spec, requirements, contracts]
    examples:
      - "Freeze requirements into SPEC"
      - "Define spec contracts"

  - name: spec-contract-diff
    path: ./spec-contract-diff/SKILL.md
    domain: engineering
    priority: high
    auto_activate: false
    description: "Detects drift between code interfaces and spec contracts"
    tags: [spec, drift, alignment, contract]
    examples:
      - "Detect code vs SPEC drift"
      - "After implementation changes"

  - name: spec-traceability
    path: ./spec-traceability/SKILL.md
    domain: engineering
    priority: medium
    auto_activate: false
    description: "Maintains story-to-contract-to-code-to-test mapping"
    tags: [spec, traceability, mapping]
    examples:
      - "Trace requirements to code"
      - "Map user stories to tests"

domains:
  engineering:
    description: "Technical engineering tasks"
    color: "🔧"
  product:
    description: "Product and design tasks"
    color: "🎨"
  quality:
    description: "Quality and testing tasks"
    color: "🧪"
  governance:
    description: "Process governance and compliance"
    color: "⚖️"
```

#### 1.3 创建 Agent Card (A2A 兼容)

**创建文件**: `.vic-sdd/agent-card.yaml`

```yaml
# VIBE-SDD Agent Card
# ====================
# A2A Protocol 兼容格式
# 用于多 Agent 协作时的能力发现

name: vibe-sdd-agent
description: "AI-driven Spec-Driven Development agent with self-awareness and workflow enforcement"
version: "1.0"
url: "http://localhost:8080/"
defaultInputModes: ["text"]
defaultOutputModes: ["text", "markdown"]

capabilities:
  streaming: true
  pushNotifications: false
  stateTransitionHistory: true

skills:
  - id: constitution-check
    name: "Constitution Check"
    description: "Verifies rules compliance before plans, reviews, commits"
    tags: [compliance, governance, blocking]
    examples:
      - "Before generating implementation plans"
      - "Before git commits"
      - "Before phase advancement"

  - id: context-tracker
    name: "Context Tracker"
    description: "Tracks AI knowledge state and confidence at every moment"
    tags: [self-awareness, monitoring, confidence]
    examples:
      - "At task BEGIN"
      - "After every meaningful action"
      - "Before task completion"

  - id: requirements
    name: "Requirements Analyzer"
    description: "Clarifies vague requirements into structured user stories"
    tags: [requirements, clarification, user-stories]
    examples:
      - "User requirements are ambiguous"
      - "Need to define acceptance criteria"

  - id: architecture
    name: "Architecture Designer"
    description: "Makes technology stack decisions and system architecture design"
    tags: [architecture, tech-stack, design]
    examples:
      - "Need to select technology stack"
      - "Design system architecture"

  - id: design-review
    name: "Design Reviewer"
    description: "Reviews UI/UX designs for quality and consistency"
    tags: [design, ui, ux, review]
    examples:
      - "Build UI design system"
      - "Review design mockups"

  - id: debugging
    name: "Systematic Debugger"
    description: "Systematic 4-phase root cause analysis methodology"
    tags: [debugging, root-cause, quality]
    examples:
      - "Bug fix"
      - "Test failure investigation"

  - id: qa
    name: "QA Engineer"
    description: "Test-driven development and test coverage enforcement"
    tags: [testing, tdd, quality, coverage]
    examples:
      - "Write tests for new feature"
      - "Check test coverage"

  - id: sdd-orchestrator
    name: "SDD Orchestrator"
    description: "Manages SDD workflow state machine and pipeline transitions"
    tags: [orchestration, sdd, pipeline, workflow]
    examples:
      - "Manage SDD workflow"
      - "State transition between phases"

  - id: spec-architect
    name: "Spec Architect"
    description: "Builds executable specs from ambiguous requirements"
    tags: [spec, requirements, contracts]
    examples:
      - "Freeze requirements into SPEC"
      - "Define spec contracts"

  - id: spec-contract-diff
    name: "Spec Contract Diff"
    description: "Detects drift between code interfaces and spec contracts"
    tags: [spec, drift, alignment, contract]
    examples:
      - "Detect code vs SPEC drift"
      - "After implementation changes"

  - id: spec-traceability
    name: "Spec Traceability"
    description: "Maintains story-to-contract-to-code-to-test mapping"
    tags: [spec, traceability, mapping]
    examples:
      - "Trace requirements to code"
      - "Map user stories to tests"

corordinates:
  - type: orchestrator
    name: "VIBE-SDD Orchestrator"
    description: "Coordinates all skills and manages workflow"

authentication:
  supported: false
  type: none

# 用于多 Agent 协作时的能力协商
negotiation:
  canDelegate: true
  canCoordinate: true
  preferredProtocols: ["a2a", "mcp"]
```

---

### 阶段 2：重构现有 Skills（P0）

#### 2.1 重构 context-tracker

**修改文件**: `skills/context-tracker/SKILL.md`

将当前内容拆分为 L1/L2，并创建 references/ 子目录：

```markdown
---
name: context-tracker
description: Tracks AI knowledge state and confidence at every moment.
metadata:
  domain: engineering
  version: "1.0"
  tags: [self-awareness, monitoring, confidence, blockers]
  examples:
    - "At task BEGIN"
    - "After every meaningful action"
    - "Before task completion"
  priority: critical
  auto_activate: true
---

# Context Tracker

## Overview

Unified self-awareness skill. Tracks what AI knows, infers, assumes, and doesn't know. Maintains confidence score and identifies blockers.

**Replaces:** knowledge-boundary.yaml, decision-guardrails.yaml, signal-register.yaml, exploration-journal.yaml
**State file:** `.vic-sdd/context.yaml`

## L1: When to Use

| Moment | Use Case |
|--------|----------|
| Task BEGIN | Initialize context, check blockers |
| After every action | Record signals, recalculate confidence |
| After decisions | Document alternatives and choices |
| Task END | Finalize context, emit confidence |

## L2: How to Use

### Step 1: Read current context
Read `.vic-sdd/context.yaml`

### Step 2: Update knowledge map
- Move `known` → verified facts (highest confidence)
- Move `inferred` → inferred from patterns (needs verification)
- Move `assumed` → assumptions (high risk, verify soon)
- Move `unknown` → knowledge gaps (blockers)

### Step 3: Record signals
```yaml
signals:
  positive: []    # code_created, test_passed, refactoring_done
  warnings: []    # assumption_made, edge_case_found
  blockers: []    # spec_unaligned, unknown_blocking
```

### Step 4: Calculate confidence
```
confidence = (positive - warnings×0.3 - blockers×0.5) / max_signals

> 0.7    → 🟢 HIGH   → Continue
0.4-0.7  → 🟡 MODERATE → Continue, monitor warnings
< 0.4    → 🔴 LOW   → Pause, resolve blockers
blockers >= 2 → 🛑 STOP → Ask human
```

### Step 5: Write context.yaml
Update `.vic-sdd/context.yaml` with changes

[参考: references/confidence-formula.md]

## Blocker Types

| Blocker | Meaning | Action |
|---------|---------|--------|
| `spec_unaligned` | Code vs SPEC mismatch | Must fix or update SPEC |
| `unknown_blocking` | Unknown issue blocking progress | Ask human |
| `decision_blocking` | Need decision to continue | Request clarification |
| `env_blocking` | Environment issue | Fix environment |

[参考: references/blocker-types.md]
```

**创建目录**: `skills/context-tracker/references/`

**创建文件**: `skills/context-tracker/references/confidence-formula.md`

```markdown
# Confidence Formula

## 公式

```
confidence = (positive - warnings×0.3 - blockers×0.5) / max_signals
```

## 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `positive` | int | 正面信号数量 |
| `warnings` | int | 警告信号数量 |
| `blockers` | int | 阻断信号数量 |
| `max_signals` | int | 总信号数量 (positive + warnings + blockers) |

## 阈值

| 范围 | 状态 | 行为 |
|------|------|------|
| > 0.7 | 🟢 HIGH | 继续工作 |
| 0.4-0.7 | 🟡 MODERATE | 继续但监控警告 |
| < 0.4 | 🔴 LOW | 暂停，解决阻断 |
| blockers >= 2 | 🛑 STOP | 停止，等待人类 |

## 正面信号

| 信号 | 含义 |
|------|------|
| `code_created` | 创建了代码 |
| `test_created` | 创建了测试 |
| `test_passed` | 测试通过 |
| `refactoring_done` | 重构成功 |
| `bug_fixed` | 修复了 bug |
| `spec_aligned` | 代码与 SPEC 对齐 |
| `deps_added` | 添加了依赖 |
| `docs_updated` | 更新了文档 |

## 警告信号

| 信号 | 含义 |
|------|------|
| `assumption_made` | 使用了未验证的假设 |
| `edge_case_found` | 发现边缘情况 |
| `complexity_increased` | 代码复杂度增加 |
| `deps_added` | 添加了新依赖 |
| `confidence_dropped` | 信心度下降 |

## 阻断信号

| 信号 | 含义 |
|------|------|
| `spec_unaligned` | 代码与 SPEC 不对齐 |
| `unknown_blocking` | 未知问题阻断进度 |
| `decision_blocking` | 需要决策才能继续 |
| `spec_unclear` | SPEC 不清晰 |
| `env_blocking` | 环境问题 |
```

**创建文件**: `skills/context-tracker/references/blocker-types.md`

```markdown
# Blocker Types Reference

## 完整 Blocker 列表

### spec_unaligned
- **含义**: 代码与 SPEC 不对齐
- **严重度**: 🔴 阻断
- **必须操作**: 
  1. 运行 `vic spec diff` 查看变化
  2. 选择：更新 SPEC 或修复代码
  3. 重新运行 constitution-check

### unknown_blocking
- **含义**: 未知问题阻断进度
- **严重度**: 🔴 阻断
- **必须操作**: 
  1. 记录具体问题
  2. 请求人类澄清
  3. 不要猜测继续

### decision_blocking
- **含义**: 需要决策才能继续
- **严重度**: 🟡 高
- **必须操作**:
  1. 列出所有选项
  2. 分析每个选项的利弊
  3. 请求决策

### spec_unclear
- **含义**: SPEC 不清晰
- **严重度**: 🟡 高
- **必须操作**:
  1. 识别不清晰的部分
  2. 请求澄清
  3. 不要基于假设继续

### env_blocking
- **含义**: 环境问题
- **严重度**: 🟡 高
- **必须操作**:
  1. 诊断环境问题
  2. 修复环境
  3. 验证修复

## Blocker 解决流程

```
检测到 blocker
    ↓
分类 blocker 类型
    ↓
执行对应操作
    ↓
验证解决
    ↓
重新计算 confidence
    ↓
confidence >= 0.4? ──否──→ 继续解决
    ↓是
继续工作
```
```

#### 2.2 重构 constitution-check

**修改文件**: `skills/constitution-check/SKILL.md`

```markdown
---
name: constitution-check
description: Verifies rules compliance before plans, reviews, commits.
metadata:
  domain: governance
  version: "1.0"
  tags: [compliance, governance, blocking, constitution]
  examples:
    - "Before generating implementation plans"
    - "Before git commits"
    - "Before phase advancement"
  priority: critical
  auto_activate: false
---

# Constitution Check

## Overview

Checks `.vic-sdd/constitution.yaml` for rule violations and generates a compliance report. **MANDATORY** before:
- Generating implementation plans
- Code reviews
- Phase advancement
- Git commits

## L1: When to Use

| Situation | Required? |
|-----------|-----------|
| Before `writing-plans` | ✅ Mandatory |
| Before `subagent-driven-development` | ✅ Mandatory |
| Before `requesting-code-review` | ✅ Mandatory |
| Before `finishing-a-development-branch` | ✅ Mandatory |
| After `spec-contract-diff` detected drift | ✅ Mandatory |
| Any phase advancement | ✅ Mandatory |

## L2: How to Use

### Step 1: Read Constitution
Read `.vic-sdd/constitution.yaml`

### Step 2: Check Each Rule

For each principle in constitution.yaml:

```markdown
## Checking: [PRINCIPLE-ID]

Rule: [the actual rule text]

Verifiable: [true/false]
Checker: [the checker command if verifiable]

Result: ✅ PASS / ⚠️ WARNING / 🔴 BLOCKER
```

### Step 3: Generate Report

```markdown
# Constitution Compliance Report
> Checked at: YYYY-MM-DD HH:MM:SS

## Summary

| Rule | Status | Severity |
|------|--------|----------|
| SPEC-FIRST | ✅ PASS | critical |
| SPEC-ALIGNED | 🔴 BLOCKER | critical |

## Blockers (must fix before continuing)

| ID | Rule | Action Required |
|----|------|----------------|
| SPEC-ALIGNED | Code vs SPEC mismatch | Update SPEC or fix code |
```

### Step 4: Resolve Blockers

**SPEC-ALIGNED blocker**:
1. Option A: Update SPEC (preferred)
2. Option B: Revert code (emergency)
3. Option C: Document as accepted drift

### Step 5: Re-check

Run constitution-check again until all blockers resolved.

[参考: references/blocker-resolution.md]
```

**创建目录**: `skills/constitution-check/references/`

**创建文件**: `skills/constitution-check/references/blocker-resolution.md`

```markdown
# Constitution Blocker Resolution

## SPEC-ALIGNED Blocker

### Option A: Update SPEC (Preferred)

```bash
# 1. Run diff to see changes
vic spec diff

# 2. Identify affected sections
# 3. Update SPEC-ARCHITECTURE.md or SPEC-REQUIREMENTS.md
# 4. Re-run constitution-check
```

### Option B: Revert Code (Emergency Only)

```bash
# 1. Identify code changes
git diff [affected files]

# 2. Revert to match SPEC
git checkout -- [affected files]

# 3. Re-run constitution-check
```

### Option C: Document as Accepted Drift

```yaml
# Add to .vic-sdd/risk-zones.yaml
drift记录:
  - id: DRIFT-[DATE]
    date: YYYY-MM-DD
    description: "What changed and why SPEC wasn't updated"
    sections_affected: ["SPEC-ARCHITECTURE.md §3.2"]
    approved_by: [pending human approval]
```

⚠️ Only for emergency hotfixes where there's no time to update SPEC.

## GATE-BEFORE-COMMIT Blocker

```bash
# 1. Run gate checks
vic spec gate 0
vic spec gate 1
vic spec gate 2
vic spec gate 3

# 2. Fix failures
# 3. Re-run constitution-check
```

## NO-HARDCODED-SECRETS Blocker

```bash
# 1. Find secrets
grep -rn "api_key\|password\|secret" --include="*.go" ./cmd/

# 2. Move to environment variables
# 3. Update config loading
# 4. Re-run constitution-check
```
```

---

### 阶段 3：重构其余 Skills（P1）

#### 3.1 统一格式 - 其余 9 个 Skills

对以下技能应用相同的 L1/L2 重构：

- `requirements` → references/requirements.md
- `architecture` → references/architecture.md
- `design-review` → references/design-review.md
- `debugging` → references/debugging.md
- `qa` → references/qa.md
- `sdd-orchestrator` → references/sdd-orchestrator.md
- `spec-architect` → references/spec-architect.md
- `spec-contract-diff` → references/spec-contract-diff.md
- `spec-traceability` → references/spec-traceability.md

#### 3.2 创建 Skill 使用统计

**创建文件**: `skills/usage-stats.yaml`

```yaml
# Skill Usage Statistics
# 用于分析和优化技能系统

version: "1.0"
updated: 2026-03-21

# 按 domain 统计
domains:
  governance:
    skills: [constitution-check]
    avg_activation_time: "2-5 min"
    
  engineering:
    skills: [context-tracker, architecture, debugging, sdd-orchestrator, spec-architect, spec-contract-diff, spec-traceability]
    avg_activation_time: "5-10 min"
    
  product:
    skills: [requirements, design-review]
    avg_activation_time: "10-15 min"
    
  quality:
    skills: [qa]
    avg_activation_time: "15-30 min"

# 优先级分布
priority_distribution:
  critical: 2   # constitution-check, context-tracker
  high: 5       # requirements, architecture, debugging, qa, spec-architect, spec-contract-diff
  medium: 3     # design-review, spec-traceability
  low: 0

# 自动激活技能
auto_activate:
  - context-tracker  # 始终活跃，跟踪状态
```

---

### 阶段 4：更新文档（P1）

#### 4.1 更新 AGENTS.md

更新目录结构说明，反映新的 skills 系统：

```markdown
skills/                    # 11个核心技能 (Google Cloud Agent Skills 规范)
├── registry.yaml          # Skill Registry (能力发现注册表)
├── _template/             # Skill 标准模板
│   └── SKILL.md
├── constitution-check/    # 合规检查 (critical)
│   ├── SKILL.md          # L1 + L2 指令
│   └── references/       # L3 按需资源
├── context-tracker/      # 自我认知 (critical, auto_activate)
│   ├── SKILL.md
│   └── references/
├── requirements/         # 需求分析 (high)
│   ├── SKILL.md
│   └── references/
├── architecture/        # 架构设计 (high)
│   ├── SKILL.md
│   └── references/
├── design-review/       # 设计审查 (medium)
│   ├── SKILL.md
│   └── references/
├── debugging/           # 调试 (high)
│   ├── SKILL.md
│   └── references/
├── qa/                  # 测试 (high)
│   ├── SKILL.md
│   └── references/
├── sdd-orchestrator/    # SDD编排 (critical)
│   ├── SKILL.md
│   └── references/
├── spec-architect/      # 规范编写 (high)
│   ├── SKILL.md
│   └── references/
├── spec-contract-diff/  # 差异检测 (high)
│   ├── SKILL.md
│   └── references/
└── spec-traceability/  # 追溯追踪 (medium)
    ├── SKILL.md
    └── references/

.vic-sdd/
├── agent-card.yaml       # A2A Agent Card (多Agent协作)
```

#### 4.2 创建 Skills 使用指南

**创建文件**: `docs/SKILLS_GUIDE.md`

```markdown
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
  examples: ["Example 1", "Example 2"]
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

## 使用流程

1. **Agent 启动** → 读取 Agent Card → 发现可用技能
2. **任务到来** → 查询 Registry → 选择合适技能
3. **技能激活** → 加载 SKILL.md L1+L2 → 执行指令
4. **需要深入** → 加载 references/ → 获取详细信息
5. **任务完成** → 更新 context.yaml → 返回结果
```

---

## 文件变更清单

### 新增文件 (按阶段)

#### 阶段 1
| 文件 | 说明 |
|------|------|
| `skills/_template/SKILL.md` | Skill 标准模板 |
| `skills/registry.yaml` | Skill Registry |
| `.vic-sdd/agent-card.yaml` | A2A Agent Card |

#### 阶段 2
| 文件 | 说明 |
|------|------|
| `skills/context-tracker/SKILL.md` | 重构 L1/L2 |
| `skills/context-tracker/references/confidence-formula.md` | 信心度公式详解 |
| `skills/context-tracker/references/blocker-types.md` | Blocker 类型参考 |
| `skills/constitution-check/SKILL.md` | 重构 L1/L2 |
| `skills/constitution-check/references/blocker-resolution.md` | Blocker 解决指南 |

#### 阶段 3
| 文件 | 说明 |
|------|------|
| `skills/*/references/*.md` | 9个技能的 references |

#### 阶段 4
| 文件 | 说明 |
|------|------|
| `docs/SKILLS_GUIDE.md` | Skills 使用指南 |
| `skills/usage-stats.yaml` | 技能使用统计 |

### 修改文件
| 文件 | 改动 |
|------|------|
| `AGENTS.md` | 更新目录结构说明 |
| 11个 `SKILL.md` | L1/L2 重构 |

---

## 实施顺序

```
Week 1:
  ├── 阶段 1: 建立标准
  │   ├── 创建 _template/SKILL.md
  │   ├── 创建 registry.yaml
  │   └── 创建 agent-card.yaml
  │
  └── 阶段 2: 重构核心 Skills (2个 critical)
      ├── 重构 context-tracker
      ├── 创建 references/
      ├── 重构 constitution-check
      └── 创建 references/

Week 2:
  └── 阶段 3: 重构其余 9 个 Skills
      ├── requirements + references
      ├── architecture + references
      ├── design-review + references
      ├── debugging + references
      ├── qa + references
      ├── sdd-orchestrator + references
      ├── spec-architect + references
      ├── spec-contract-diff + references
      └── spec-traceability + references

Week 3:
  └── 阶段 4: 文档和验证
      ├── 更新 AGENTS.md
      ├── 创建 SKILLS_GUIDE.md
      ├── 创建 usage-stats.yaml
      └── 验证所有 Skills 符合规范
```

---

## 验收标准

### L1 检查
- [ ] 每个 SKILL.md 有完整 metadata
- [ ] description 不超过 2 句话
- [ ] tags 包含 2-5 个标签
- [ ] examples 包含 2-3 个示例

### L2 检查
- [ ] L1: When to Use 表格完整
- [ ] L2: How to Use 有明确步骤
- [ ] 参考 references/ 的链接正确

### L3 检查
- [ ] references/ 目录存在
- [ ] 至少包含 1 个参考文件
- [ ] 详细内容不膨胀核心 SKILL.md

### Registry 检查
- [ ] registry.yaml 包含所有 11 个技能
- [ ] domain/priority/tags 正确
- [ ] auto_activate 标志正确

### Agent Card 检查
- [ ] 包含所有 11 个 skill 定义
- [ ] 符合 A2A 协议格式
- [ ] capabilities 正确定义

---

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| Skill 数量增加复杂 | 中 | 保持 registry.yaml 单一来源 |
| references 膨胀 | 低 | 只放详细指南，核心在 SKILL.md |
| 多 Agent 协作测试困难 | 高 | 先在单 Agent 环境验证 |

---

**下一步**: 开始阶段 1 — 建立目录结构标准
