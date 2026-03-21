# VIBE-SDD Skills 系统优化计划

> **生成时间**: 2026-03-21
> **状态**: 待执行
> **目标**: 基于评估结果，优化 Skills 系统以提高实际工作流效率

---

## 问题诊断

基于重新评估，以下是关键问题：

| 问题 | 严重度 | 影响 |
|------|--------|------|
| **技能数量膨胀** (11个) | 🔴 高 | AI 选择困难，执行负担 |
| **状态文件分散** (5+ 个) | 🔴 高 | AI 记忆负担增加 |
| **auto_activate 不明确** | 🟡 中 | 触发时机模糊 |
| **Registry/Agent Card 实际价值有限** | 🟡 中 | 单 Agent 场景下多余 |
| **L3 加载判断模糊** | 🟡 中 | AI 不知何时加载 references |

---

## 优化目标

```
优化前:                               优化后:
11 个 Skills                         5 个 Skills
5+ 个状态文件                         1 个状态文件
模糊的激活时机                        明确的激活时机
分散的工作流                          统一的工作流
单 Agent 冗余结构                     按需的多层结构
```

---

## 优化方案

### 核心策略

1. **技能合并** (11 → 5): 减少选择负担
2. **状态统一**: 多文件 → 单文件
3. **激活时机明确化**: 消除模糊性
4. **L3 按需变强制**: references/ 作为技能的标准部分
5. **移除冗余**: 单 Agent 场景下不必要的结构

---

## 实施阶段

### 阶段 1：技能合并 (11 → 5)

#### 合并方案

```
当前 (11 个):
├── constitution-check        → 合并到 unified-workflow
├── context-tracker          → 保持独立
├── requirements             → 合并到 spec-workflow
├── architecture             → 合并到 spec-workflow
├── design-review           → 合并到 spec-workflow
├── debugging               → 合并到 implementation
├── qa                      → 合并到 implementation
├── sdd-orchestrator        → 合并到 unified-workflow
├── spec-architect          → 合并到 spec-workflow
├── spec-contract-diff      → 合并到 unified-workflow
└── spec-traceability       → 合并到 unified-workflow

建议 (5 个):
├── context-tracker          → 自我认知（始终活跃）
├── spec-workflow            → 需求→架构→SPEC
├── implementation          → 调试→测试→代码
├── unified-workflow         → SDD编排+Constitution+Traceability
└── quick                   → 简单任务（替代所有 single-file 场景）
```

#### 合并详细设计

##### 1. context-tracker (保持)

```
skills/context-tracker/
├── SKILL.md               # L1/L2
└── references/
    ├── confidence-formula.md
    └── blocker-types.md
```

**保持不变**：`context-tracker` 是唯一 `auto_activate: true` 的技能。

##### 2. spec-workflow (合并: requirements + architecture + design-review + spec-architect)

```markdown
---
name: spec-workflow
description: Handles requirements analysis, architecture design, and SPEC creation.
metadata:
  domain: product
  version: "1.0"
  tags: [requirements, architecture, spec, design]
  examples:
    - "User requirements are ambiguous"
    - "Need to design system architecture"
    - "Freeze requirements into SPEC"
  priority: critical
  auto_activate: false
---

# SPEC Workflow

## Overview

Handles the complete workflow from vague requirements to frozen SPEC. Combines requirements analysis, architecture design, and SPEC creation.

**Merged from:** requirements + architecture + design-review + spec-architect

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Requirements are vague or ambiguous | ✅ Yes |
| Need to design system architecture | ✅ Yes |
| Create or update SPEC documents | ✅ Yes |
| UI/UX design decisions | ✅ Yes |
| Simple code changes (no spec needed) | ❌ No |
| Debugging existing code | ❌ No |

## L2: How to Use

### Phase 1: Requirements Analysis

1. **Clarify Requirements**
   - Identify vague parts
   - Ask clarifying questions
   - Define acceptance criteria

2. **Create User Stories**
   - Format: "As a [role], I want [feature], so that [value]"
   - Include priority (P0/P1/P2)
   - Define acceptance criteria

### Phase 2: Architecture Design

3. **Design System Architecture**
   - Select technology stack
   - Define module structure
   - Design API contracts
   - Consider scalability

### Phase 3: SPEC Creation

4. **Create SPEC Documents**
   - SPEC-REQUIREMENTS.md (user stories, acceptance criteria)
   - SPEC-ARCHITECTURE.md (design, tech stack, modules)

5. **Validate SPEC**
   - Run `vic spec gate 0` (requirements completeness)
   - Run `vic spec gate 1` (architecture completeness)
   - Fix any issues

[参考: references/spec-workflow-guide.md]
```

##### 3. implementation (合并: debugging + qa + spec-contract-diff)

```markdown
---
name: implementation
description: Handles code implementation, debugging, testing, and SPEC alignment.
metadata:
  domain: engineering
  version: "1.0"
  tags: [implementation, debugging, testing, coding]
  examples:
    - "Implement a new feature"
    - "Fix a bug"
    - "Write tests for code"
    - "Check code vs SPEC alignment"
  priority: critical
  auto_activate: false
---

# Implementation Workflow

## Overview

Handles the complete implementation lifecycle from coding to testing to SPEC alignment.

**Merged from:** debugging + qa + spec-contract-diff

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Implementing new feature | ✅ Yes |
| Fixing a bug | ✅ Yes |
| Writing or running tests | ✅ Yes |
| Checking code vs SPEC alignment | ✅ Yes |
| Designing system architecture | ❌ No (use spec-workflow) |
| Clarifying requirements | ❌ No (use spec-workflow) |

## L2: How to Use

### Option A: Feature Implementation

1. **Read SPEC**
   - Read SPEC-ARCHITECTURE.md
   - Read SPEC-REQUIREMENTS.md

2. **Implement Code**
   - Follow TDD: Write test first
   - Run: `vic tdd start --feature "[feature]"`

3. **Check Alignment**
   - Run: `vic spec gate 2`
   - If failed: Fix alignment

4. **Run Tests**
   - Run: `vic spec gate 3`
   - If failed: Fix tests

### Option B: Bug Fix

1. **Diagnose**
   - Run: `vic debug start --problem "[description]"`

2. **Follow Debug Cycle**
   - Survey → Pattern → Hypothesis → Implement

3. **Verify Fix**
   - Run tests
   - Check SPEC alignment

### Option C: Test Coverage

1. **Check Coverage**
   - Run: `vic qa quick`

2. **Improve Coverage**
   - Add missing tests
   - Run: `vic tdd red --test "[test]"`

[参考: references/implementation-guide.md]
```

##### 4. unified-workflow (合并: constitution-check + sdd-orchestrator + spec-traceability)

```markdown
---
name: unified-workflow
description: Orchestrates SDD workflow, enforces Constitution rules, and maintains traceability.
metadata:
  domain: governance
  version: "1.0"
  tags: [sdd, orchestration, constitution, traceability, gates]
  examples:
    - "Start a new feature delivery"
    - "Advance SDD phase"
    - "Check before commit"
    - "Verify requirements-to-code mapping"
  priority: critical
  auto_activate: false
---

# Unified Workflow

## Overview

Single controller for SDD workflow, Constitution enforcement, and traceability tracking.

**Merged from:** constitution-check + sdd-orchestrator + spec-traceability

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Start new feature delivery | ✅ Yes |
| Advance SDD phase | ✅ Yes |
| Before git commit | ✅ Yes |
| Check requirements traceability | ✅ Yes |
| During implementation | ❌ No (use implementation) |
| Clarifying requirements | ❌ No (use spec-workflow) |

## L2: How to Use

### Workflow: Feature Delivery

1. **Start Delivery**
   ```bash
   vic auto start
   ```

2. **Check Constitution**
   - Run: `constitution-check`
   - Fix any blockers

3. **Manage SDD Phases**
   - Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady

4. **Gate Checks at Each Phase**
   - Gate 0: Requirements completeness
   - Gate 1: Architecture completeness
   - Gate 2: Code alignment
   - Gate 3: Test coverage

5. **Traceability Check**
   - Verify: requirements → SPEC → code → tests

6. **End Delivery**
   ```bash
   vic auto stop
   ```

### Workflow: Pre-Commit Check

1. **Run Constitution Check**
   ```bash
   constitution-check
   ```

2. **Run Gate Checks**
   ```bash
   vic gate check --blocking
   ```

3. **Fix Issues if Any**
   - Resolve blockers
   - Update SPEC if needed

### Workflow: Traceability Check

1. **Read Traceability Map**
   - User Story → SPEC Contract → Code → Tests

2. **Verify Mapping**
   - Each requirement has implementation
   - Each implementation has tests

3. **Update if Needed**
   - Add missing mappings
   - Remove orphaned code

[参考: references/unified-workflow-guide.md]
```

##### 5. quick (新增)

```markdown
---
name: quick
description: Handles simple, single-file changes that don't require full SDD workflow.
metadata:
  domain: engineering
  version: "1.0"
  tags: [quick, simple, single-file, trivial]
  examples:
    - "Fix a typo"
    - "Rename a variable"
    - "Add a comment"
    - "Simple refactor (single file)"
  priority: medium
  auto_activate: false
---

# Quick Workflow

## Overview

Handles trivial tasks that don't need full SDD workflow. Use when:
- Single file change
- Clear scope
- No SPEC update needed

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Fix a typo | ✅ Yes |
| Rename a variable | ✅ Yes |
| Add comments | ✅ Yes |
| Simple single-file refactor | ✅ Yes |
| Multi-file changes | ❌ No (use implementation) |
| New feature | ❌ No (use spec-workflow) |
| Bug fix | ⚠️ Maybe (use implementation if complex) |

## L2: How to Use

1. **Verify Scope**
   - Confirm single file
   - Confirm no SPEC impact

2. **Make Change**
   - Edit file
   - Run tests if applicable

3. **Quick Verification**
   - Check diagnostics
   - Commit if clean
```

---

### 阶段 2：状态文件统一 (5+ → 1)

#### 当前状态文件

```
.vic-sdd/
├── context.yaml              # context-tracker
├── constitution.yaml          # constitution-check
├── risk-zones.yaml           # 风险管理
├── dependency-graph.yaml      # 依赖图
├── SPEC-REQUIREMENTS.md       # 需求规范
├── SPEC-ARCHITECTURE.md       # 架构规范
├── status/
│   ├── events.yaml
│   ├── state.yaml
│   ├── spec-hash.json
│   └── ...
└── tech/
    └── tech-records.yaml
```

#### 建议：统一状态文件

```yaml
# .vic-sdd/state.yaml

version: "1.0"
updated: "2026-03-21"

# === Context (from context-tracker) ===
context:
  known: []
  inferred: []
  assumed: []
  unknown: []
  confidence:
    score: 0.0
    positive_signals: 0
    warning_signals: 0
    blocker_signals: 0

# === Compliance (from constitution-check) ===
compliance:
  constitution_hash: ""
  last_check: ""
  violations: []
  blockers: []

# === SPEC State ===
spec:
  requirements_hash: ""
  architecture_hash: ""
  last_gate_passed: 0
  drift_detected: false
  drift_sections: []

# === SDD Workflow State ===
workflow:
  current_phase: ""
  current_feature: ""
  auto_mode: false
  last_transition: ""

# === Traceability ===
traceability:
  requirements: []
  contracts: []
  implementations: []
  tests: []

# === Risks ===
risks:
  - id: ""
    area: ""
    description: ""
    status: ""

# === Tech Decisions ===
tech_decisions:
  - id: ""
    title: ""
    decision: ""
    status: ""

# === Dependencies ===
dependencies:
  last_scan: ""
  graph_hash: ""
```

#### 迁移策略

1. **Phase 1: 创建 state.yaml** (新文件)
2. **Phase 2: 更新所有技能** (读取/写入 state.yaml)
3. **Phase 3: 废弃旧文件** (保留备份，删除旧文件)
4. **Phase 4: 更新 CLI** (vic 命令读取 state.yaml)

---

### 阶段 3：auto_activate 明确化

#### 当前问题

```
auto_activate: true  # 何时触发？不清楚
```

#### 建议：定义明确的触发规则

```yaml
# skills/registry.yaml (更新)

skills:
  - name: context-tracker
    auto_activate:
      enabled: true
      triggers:
        - session_start: "每次对话开始"
        - before_planning: "规划前"
        - after_code_change: "代码变更后"
        - after_decision: "重大决策后"
        - task_end: "任务完成前"
      
  - name: unified-workflow
    auto_activate:
      enabled: false
      triggers:
        - explicit_invocation: "明确调用"
        - pre_commit: "提交前"
        - phase_change: "阶段变更"
```

#### 在 SKILL.md 中定义触发规则

```markdown
## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Session starts | ⚡ auto_activate (context-tracker) |
| Before planning | ✅ Yes (use spec-workflow) |
| Before commit | ✅ Yes (use unified-workflow) |
| During implementation | ✅ Yes (use implementation) |
| After implementation | ✅ Yes (use unified-workflow) |

## L1: Auto-Activate Triggers

This skill is activated automatically when:
- User explicitly invokes it
- `vic auto start` is called
- `vic gate check --blocking` is run
```

---

### 阶段 4：L3 references/ 强化

#### 当前问题

```
L3 (references/) 是"按需加载"
→ AI 不知道何时加载
→ references/ 可能被忽略
```

#### 建议：L3 作为技能的强制部分

```markdown
---
name: example-skill
description: Example skill with mandatory references.
metadata:
  domain: engineering
  version: "1.0"
  tags: [example]
  examples:
    - "Example usage"
  priority: high
  auto_activate: false
---

# Example Skill

## L2: How to Use

### Step 1: Read Quick Guide
Read `references/quick-guide.md` (5 min read)

### Step 2: Execute Steps
Follow the steps in quick-guide.md

### Step 3: (If needed) Read Full Guide
Read `references/full-guide.md` for advanced topics

### Step 4: Verify
Run: `vic check`
```

**改动**：不再是"按需加载"，而是"分层阅读"：
- L2 → quick-guide.md (必读)
- L3 → full-guide.md (可选深入)

---

### 阶段 5：简化 Agent Card (多 Agent 场景保留)

#### 当前问题

```
agent-card.yaml 包含 11 个技能的完整定义
→ 单 Agent 场景下价值有限
→ 但为多 Agent 保留了复杂性
```

#### 建议：分离单 Agent 和多 Agent 用途

```yaml
# .vic-sdd/agent-card.yaml (简化版，单 Agent 用)

name: vibe-sdd-agent
description: "VIBE-SDD single agent for spec-driven development"
version: "1.0"
skills:
  - context-tracker
  - spec-workflow
  - implementation
  - unified-workflow
  - quick

# .vic-sdd/agent-card-full.yaml (完整版，多 Agent 用)

name: vibe-sdd-agent
description: "VIBE-SDD agent with full capabilities"
version: "1.0"
capabilities:
  multi_agent: true
skills:
  - id: context-tracker
    name: "Context Tracker"
    description: "..."
    can_delegate_to: []
    
  - id: spec-workflow
    name: "SPEC Workflow"
    description: "..."
    can_delegate_to: ["requirements_agent", "architecture_agent"]
    
  - id: implementation
    name: "Implementation"
    description: "..."
    can_delegate_to: ["debugging_agent", "qa_agent"]
    
  - id: unified-workflow
    name: "Unified Workflow"
    description: "..."
    can_delegate_to: []
```

---

## 文件变更清单

### 阶段 1：技能合并

#### 删除的技能 (6 个)

| 删除 | 合并到 |
|------|--------|
| `skills/requirements/` | `skills/spec-workflow/` |
| `skills/architecture/` | `skills/spec-workflow/` |
| `skills/design-review/` | `skills/spec-workflow/` |
| `skills/spec-architect/` | `skills/spec-workflow/` |
| `skills/debugging/` | `skills/implementation/` |
| `skills/qa/` | `skills/implementation/` |
| `skills/spec-contract-diff/` | `skills/implementation/` |
| `skills/constitution-check/` | `skills/unified-workflow/` |
| `skills/sdd-orchestrator/` | `skills/unified-workflow/` |
| `skills/spec-traceability/` | `skills/unified-workflow/` |

#### 保留/新增的技能 (5 个)

| 技能 | 来源 | 目录 |
|------|------|------|
| `context-tracker` | 保留 | `skills/context-tracker/` |
| `spec-workflow` | 新建 | `skills/spec-workflow/` |
| `implementation` | 新建 | `skills/implementation/` |
| `unified-workflow` | 新建 | `skills/unified-workflow/` |
| `quick` | 新建 | `skills/quick/` |

#### 新增文件

| 文件 | 说明 |
|------|------|
| `skills/spec-workflow/SKILL.md` | 合并后的 SPEC 工作流 |
| `skills/spec-workflow/references/spec-workflow-guide.md` | 详细指南 |
| `skills/implementation/SKILL.md` | 合并后的实现工作流 |
| `skills/implementation/references/implementation-guide.md` | 详细指南 |
| `skills/unified-workflow/SKILL.md` | 合并后的统一工作流 |
| `skills/unified-workflow/references/unified-workflow-guide.md` | 详细指南 |
| `skills/quick/SKILL.md` | 快速任务工作流 |
| `skills/quick/references/quick-guide.md` | 快速任务指南 |

### 阶段 2：状态文件统一

| 文件 | 操作 |
|------|------|
| `.vic-sdd/state.yaml` | 新建（统一状态） |
| `.vic-sdd/context.yaml` | 废弃（迁移到 state.yaml）|
| `.vic-sdd/constitution.yaml` | 保留（但结构合并到 state.yaml）|
| `.vic-sdd/risk-zones.yaml` | 保留（但结构合并到 state.yaml）|
| `cmd/vic-go/internal/commands/` | 更新（读取 state.yaml）|

### 阶段 3：触发规则明确化

| 文件 | 改动 |
|------|------|
| `skills/registry.yaml` | 更新 auto_activate 定义 |
| 5 个 SKILL.md | 添加 L1: Auto-Activate Triggers |

### 阶段 4：L3 references/ 强化

| 文件 | 改动 |
|------|------|
| 5 个 SKILL.md | L2 中添加"必读"标记 |
| `skills/_template/SKILL.md` | 更新模板 |

### 阶段 5：Agent Card 简化

| 文件 | 操作 |
|------|------|
| `.vic-sdd/agent-card.yaml` | 简化为单 Agent 版 |
| `.vic-sdd/agent-card-full.yaml` | 新建多 Agent 完整版 |

---

## 实施顺序

```
Week 1:
  └── 阶段 1: 技能合并
      ├── Day 1: 创建 spec-workflow (合并 requirements + architecture + design-review + spec-architect)
      ├── Day 2: 创建 implementation (合并 debugging + qa + spec-contract-diff)
      ├── Day 3: 创建 unified-workflow (合并 constitution-check + sdd-orchestrator + spec-traceability)
      ├── Day 4: 创建 quick (新技能)
      └── Day 5: 删除旧技能目录，更新 registry.yaml

Week 2:
  ├── 阶段 2: 状态文件统一
  │   ├── Day 6: 创建 state.yaml 结构
  │   ├── Day 7: 更新 context-tracker
  │   └── Day 8: 更新 unified-workflow
  │
  └── 阶段 3: 触发规则明确化
      ├── Day 9: 更新 registry.yaml
      └── Day 10: 更新 5 个 SKILL.md

Week 3:
  ├── 阶段 4: L3 references/ 强化
  │   └── Day 11: 更新所有 SKILL.md 和模板
  │
  └── 阶段 5: Agent Card 简化
      ├── Day 12: 简化 agent-card.yaml
      └── Day 13: 创建 agent-card-full.yaml

Week 4:
  └── 验证和文档
      ├── Day 14: 更新 SKILLS_GUIDE.md
      ├── Day 15: 更新 AGENTS.md
      └── Day 16: 全面验证
```

---

## 验收标准

### 阶段 1 验收

- [ ] 11 个技能 → 5 个技能
- [ ] registry.yaml 更新
- [ ] 5 个 SKILL.md 符合 L1/L2 结构
- [ ] 5 个 references/ 目录存在

### 阶段 2 验收

- [ ] `state.yaml` 存在且结构正确
- [ ] `context-tracker` 读写 `state.yaml`
- [ ] `unified-workflow` 读写 `state.yaml`
- [ ] 旧状态文件已废弃

### 阶段 3 验收

- [ ] `registry.yaml` 包含触发规则
- [ ] 5 个 SKILL.md 包含 Auto-Activate Triggers

### 阶段 4 验收

- [ ] 5 个 SKILL.md L2 包含必读标记
- [ ] `_template/SKILL.md` 已更新

### 阶段 5 验收

- [ ] `agent-card.yaml` 简化为 5 个技能
- [ ] `agent-card-full.yaml` 存在

### 最终验收

- [ ] 技能数量: 11 → 5
- [ ] 状态文件: 5+ → 1
- [ ] 所有技能符合 L1/L2/L3 结构
- [ ] AGENTS.md 已更新
- [ ] SKILLS_GUIDE.md 已更新
- [ ] CLI 命令读取统一状态

---

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| 合并后的技能过于庞大 | 中 | 保持 L1/L2/L3 结构，内容分层 |
| 状态迁移丢失数据 | 高 | 保留备份，逐步迁移 |
| AI 重新学习 5 个技能 | 低 | 保持 L1/L2 结构相似 |
| 旧文件清理不完整 | 中 | 使用脚本批量删除 |

---

## 优化后预期效果

| 维度 | 优化前 | 优化后 |
|------|--------|--------|
| **技能数量** | 11 个 | **5 个** |
| **状态文件** | 5+ 个 | **1 个** |
| **AI 选择负担** | 高 | **低** |
| **AI 记忆负担** | 高 | **低** |
| **L3 加载** | 模糊 | **明确** |
| **auto_activate** | 模糊 | **明确** |
| **单 Agent 效率** | 中 | **高** |
| **多 Agent 准备** | 好 | **更好** |

---

**下一步**: 开始阶段 1 — 技能合并 (11 → 5)
