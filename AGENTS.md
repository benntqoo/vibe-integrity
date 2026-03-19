# Agent Collaboration Guide

**Updated for Vibe-SDD Development Workflow**

## Current System Status

✅ **Multi-Agent Supported**: Yes, via Git branching workflow
✅ **Multi-User Supported**: Yes, via Git collaboration
✅ **Structured Development**: Yes, via .vic-sdd/ SPEC workflow
✅ **Self-Aware AI**: Yes, via 4 self-awareness mechanisms
✅ **Pattern System**: Yes, via Google 5-agent-design-patterns mapped to skills
✅ **Schema-Validated Outputs**: Yes, via JSON Schema for SPEC docs
✅ **Pipeline-Defined**: Yes, via pipeline_metadata in all 19 skills
❌ **Real-Time Collaboration**: No, requires Git merge workflow

---

## Google 5 Agent Design Patterns → VIBE-SDD Mapping

VIBE-SDD implements Google's 5 core agent design patterns. Each pattern maps to specific components:

| Pattern | Google Definition | VIBE-SDD Implementation | Coverage |
|---------|-------------------|-------------------------|---------|
| **Tool Wrapper** | Encapsulate capabilities with clear boundaries | `vic` CLI (25 commands) — each wraps a specific capability | ✅ 95% |
| **Generator** | Fixed-format output via templates | SPEC docs + `spec-requirements.schema.json`, `spec-architecture.schema.json` | ✅ 90% |
| **Reviewer** | Dedicated checker for quality/gaps | 8 reviewers in `reviewer.interface.yaml` (spec-contract-diff, spec-traceability, etc.) | ✅ 90% |
| **Invoke** | On-demand knowledge retrieval | `AGENTS.md` (protocol layer) + `sdd-orchestrator` (enforcement layer) | ✅ 85% |
| **Pipeline** | Sequential steps with checkpoints | All 19 skills have `pipeline_metadata` defining handoff/exit/triggers | ✅ 90% |

### Pattern → Component Reference

```
Tool Wrapper:
  vic CLI (cmd/vic-go/) → 25 commands with exact parameters and output formats
  Schemas: skills/sdd-orchestrator/sdd-machine-schema.json

Generator:
  Templates: SPEC-REQUIREMENTS.md, SPEC-ARCHITECTURE.md
  JSON Schemas: skills/spec-architect/spec-requirements.schema.json
               skills/spec-architect/spec-architecture.schema.json
  Skills: spec-architect, spec-to-codebase, vibe-think, vibe-redesign,
          vibe-architect, vibe-design, knowledge-boundary,
          test-driven-development

  Reviewer:
    Interface: skills/sdd-orchestrator/reviewer.interface.yaml
    Skills: spec-contract-diff, spec-traceability, spec-driven-test,
            vibe-qa, vibe-design, pre-decision-check, signal-register,
            knowledge-boundary, exploration-journal, vibe-debug,
            adaptive-planning

Invoke:
  Protocol: AGENTS.md (when to invoke what)
  Enforcement: sdd-orchestrator SKILL.md (enforces state transitions)

Pipeline:
  Reference: AGENTS.md Pipeline sections + Self-Awareness Activation Protocol
  Metadata: Each skill has pipeline_metadata (handoff, exit_condition, triggers)
```

### Invoke Boundary Clarification

AGENTS.md and sdd-orchestrator serve DIFFERENT layers — both are needed:

```
AGENTS.md (Protocol Layer):
  → WHOLE AI's perspective
  → Defines: "When should I invoke which skill?"
  → Mechanism: AI reads AGENTS.md → follows protocol
  → Scope: All 19 skills across all phases

sdd-orchestrator (Enforcement Layer):
  → SDD PHASE ONLY
  → Enforces: "Which skills can be invoked in which SDD state?"
  → Mechanism: State machine + gate checks
  → Scope: 7 SDD skills + gate validation
```

**Rule**: When in SDD phase, always route through `sdd-orchestrator`.
**Rule**: Outside SDD phase, follow AGENTS.md protocol directly.

---

## 核心设计原则

### AI 的自知之明

```
当前 Coding Agent 的根本问题：
─────────────────────────────────────────────────────────────
不是"AI 太笨"，而是"AI 不知道自己不知道"

当 AI 说"我理解了"时，它可能是在：
  1. 真的理解了（基于代码库的事实）
  2. 从模式推断的（可能是错的）
  3. 假设的（完全没验证）
  4. 幻觉的（编造的）
─────────────────────────────────────────────────────────────

VIC-SDD 的目标：
  • 不是监控 AI，而是确保 AI 有"自知之明"
  • 不是给 AI 下命令，而是给 AI 画边界
  • 不是事后检查，而是事前约束
```

---

## 四个核心机制

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│   1. Knowledge Boundary (认知地图)                               │
│      → AI 知道什么、推测什么、假设什么、不知道什么                    │
│                                                                   │
│   2. Pre-Decision Check (决策前自查)                              │
│      → 重大决策前自动检查边界和约束                                 │
│                                                                   │
│   3. Signal Register (信号注册)                                    │
│      → 用"证据链"代替"进度百分比"                                   │
│                                                                   │
│   4. Exploration Journal (探索日志)                                │
│      → AI 记录思考过程，避免重复探索                                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1. Knowledge Boundary（认知地图）

`.vic-sdd/knowledge-boundary.yaml`

```yaml
known:        # 验证过的事实（最高可信度）
inferred:     # 从模式推断的（需要验证）
assumed:      # 假设的（高风险）
unknown:      # 完全不知道的（可能阻塞）
```

**Skill**: `knowledge-boundary`

### 2. Pre-Decision Check（决策前自查）

`.vic-sdd/decision-guardrails.yaml`

```yaml
scope:        # 范围约束
attempts:     # 尝试次数约束
quality:      # 质量红线
signals:      # 信号约束
```

**Skill**: `pre-decision-check`

### 3. Signal Register（信号注册）

`.vic-sdd/signal-register.yaml`

```yaml
signals:
  positive:   # 正面信号
  warnings:   # 警告信号
  blockers:   # 阻塞信号
confidence:   # 信心度计算
```

**Skill**: `signal-register`

### 4. Exploration Journal（探索日志）

`.vic-sdd/exploration-journal.yaml`

```yaml
entries:
  - action: explore   # 开始探索
  - action: tried     # 尝试方法
  - action: decided   # 做出决策
  - action: learned   # 学习教训
```

**Skill**: `exploration-journal`

---

## SDD vs TDD: Which Mode to Use?

**VIBE-SDD supports two development modes. Choose the right one for the task.**

### Decision Tree (5 Questions)

```
Start: User Prompt
 │
 ├─ Q1: Does the project have SPEC/contract infrastructure?
 │       (.vic-sdd/SPEC-REQUIREMENTS.md exists?)
 │       ├─ NO  → TDD standalone mode
 │       └─ YES → Continue
 │
 ├─ Q2: Does the task involve cross-module interfaces/APIs?
 │       ├─ YES → SDD mode
 │       └─ NO  → Continue
 │
 ├─ Q3: Does the user mention contracts, APIs, or compliance?
 │       ├─ YES → SDD mode
 │       └─ NO  → Continue
 │
 ├─ Q4: Is the complexity in algorithm/logic rather than requirements?
 │       ├─ YES → TDD standalone mode
 │       └─ NO  → Continue
 │
 └─ Q5: Is the scope a single file/function?
         ├─ YES → TDD standalone mode
         └─ NO  → SDD mode (system-level)
```

### Mode Comparison

| Dimension | SDD (Spec-Driven) | TDD (Test-Driven) |
|-----------|-------------------|------------------|
| **Scope** | Multi-module / system | Single module / function |
| **Interface** | Explicit contracts | Internal (no contracts) |
| **Test direction** | Spec → Contract → Test | Test → Code → Refactor |
| **Entry** | `spec-architect` | `test-driven-development` |
| **Exit** | `sdd-release-guard` | Commit / `vibe-qa` |
| **Traceability** | SPEC → Contract → Code → Test | Test → Code |
| **Gateway** | Formal gates (Gate 0-3) | None |
| **Test location** | `.sdd-spec/tests/` | Same dir as code |

### When to Use SDD

```
✅ User mentions: API, interface, contract, multi-module
✅ Project has: SPEC-REQUIREMENTS.md, contract.json
✅ Cross-service or cross-module boundaries involved
✅ Compliance/traceability requirements
✅ Team needs formal review gates
```

### When to Use TDD

```
✅ Greenfield project (no SPEC yet)
✅ Single function / algorithm implementation
✅ Complexity is in logic, not requirements
✅ User explicitly asks for TDD / red-green-refactor
✅ Refactoring internal code with test coverage
```

### Layered Mode: SDD + TDD Together

For large projects, use **both** with clear separation:

```
┌─────────────────────────────────────────┐
│  SDD Layer — Contract Tests             │
│  Scope: Cross-module interfaces, APIs   │
│  Tool:  spec-driven-test               │
│  Tests live in: .sdd-spec/tests/       │
│  Driven by: contract.json              │
└──────────────┬──────────────────────────┘
               │ Boundary: public interface
               ▼
┌─────────────────────────────────────────┐
│  TDD Layer — Unit Tests                 │
│  Scope: Internal implementation logic   │
│  Tool:  test-driven-development         │
│  Tests live in: Same dir as code        │
│  Driven by: Red-green-refactor cycle    │
└─────────────────────────────────────────┘

Rule: TDD tests NEVER test cross-module behavior.
Rule: SDD contract tests NEVER test internal logic.
```

### Switching Modes Mid-Task

```
SDD → TDD:  When implementation reveals complex internal algorithm
            → Pause contract work, use TDD for that function
            → Resume SDD when algorithm is settled

TDD → SDD:  When exploration reveals cross-module implications
            → TDD tests become acceptance criteria in contract
            → Migrate to SDD for formal interface definition
```

---

## Development Workflow

### Phase 1: 定图纸 (Requirements)

```
Agent-Product uses vibe-think
    ↓
SPEC-REQUIREMENTS.md
    ↓
vic spec gate 0 (Gate: Requirements Completeness)
```

### Phase 2: 打地基 (Architecture)

```
Agent-Architect uses vibe-architect
    ↓
SPEC-ARCHITECTURE.md
    ↓
vic spec gate 1 (Gate: Architecture Completeness)
    ↓
Bridge → Agent-Develop enters sdd-orchestrator
```

### Phase 3: 立规矩 (Implementation)

```
sdd-orchestrator (activates self-awareness at entry)
    ↓
    ├── knowledge-boundary    (query before routing)
    ├── pre-decision-check   (gate check before transition)
    └── signal-register      (record each state)
    ↓
spec-architect → spec-to-codebase → spec-contract-diff → spec-driven-test
    ↓
vic gate pass --gate 4 (Code Compiles)
vic gate pass --gate 5 (Code Aligns SPEC)
    ↓
vic phase advance --to 3
vic gate pass --gate 6-7
    ↓
vic spec merge → PRD.md / ARCH.md / PROJECT.md
```

---

## Self-Aware AI Workflow

```
开始任务
    ↓
┌─────────────────────────────────────────┐
│  1. 照镜子 (knowledge-boundary)          │
│     → 知道什么？不知道什么？              │
│     → 有 unknown/assumed 阻塞？          │
└───────────────┬─────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  2. 决策前检查 (pre-decision-check)      │
│     → 范围检查                           │
│     → 质量红线检查                        │
│     → 信号检查                           │
└───────────────┬─────────────────────────┘
                ↓
         检查结果
         ├── ✅ PASS → 继续执行
         ├── ⚠️ WARN → 记录，继续
         ├── 🛑 STOP → 等待人类
         └── 🔴 BLOCK → 解决阻塞
                ↓
┌─────────────────────────────────────────┐
│  3. 执行任务                             │
│     → 产生信号 (signal-register)          │
│     → 记录探索 (exploration-journal)     │
└───────────────┬─────────────────────────┘
                ↓
         周期性信心度检查
         ├── confidence >= 0.7 → 继续
         ├── 0.4 <= confidence < 0.7 → 关注
         └── confidence < 0.4 → 暂停
```

---

## Self-Awareness Activation Protocol

**This is NOT optional.** Every task execution path MUST follow this protocol.

### The Four-Phase Loop

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  PHASE 1: BEGIN (Every task starts here)                                │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ skill:knowledge-boundary                                           │  │
│  │                                                                    │  │
│  │ INPUT : current task description                                   │  │
│  │ OUTPUT: categorized list (known/inferred/assumed/unknown)         │  │
│  │ FILE  : .vic-sdd/knowledge-boundary.yaml (read/write)             │  │
│  │                                                                    │  │
│  │ If unknown blocks this task → STOP, record blocker, ask human    │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                               ↓                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ skill:pre-decision-check                                           │  │
│  │                                                                    │  │
│  │ INPUT : task decision points + knowledge-boundary output          │  │
│  │ OUTPUT: PASS / WARN / STOP / BLOCK result                        │  │
│  │ FILES : .vic-sdd/decision-guardrails.yaml (read)                   │  │
│  │         .vic-sdd/signal-register.yaml (read)                      │  │
│  │                                                                    │  │
│  │ If STOP or BLOCK → record signals, do not proceed                 │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                               ↓                                          │
│  PHASE 2: EXECUTE (delegated to domain skills)                         │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ skill:signal-register  ← invoked after EVERY meaningful action   │  │
│  │ skill:exploration-journal ← invoked after exploration/decision  │  │
│  │                                                                    │  │
│  │ positive/warnings/blockers → update signal-register.yaml          │  │
│  │ explored/tried/decided → update exploration-journal.yaml          │  │
│  │ RECALCULATE confidence after each signal update                   │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                               ↓                                          │
│  PHASE 3: CHECKPOINT (after each subtask or milestone)                 │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ skill:pre-decision-check (re-entry, lightweight)                   │  │
│  │                                                                    │  │
│  │ If confidence < 0.4 → pause, resolve warnings/blockers            │  │
│  │ If blockers >= 2 → STOP, ask human                               │  │
│  │ If all clear → continue to next subtask                           │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                               ↓                                          │
│  PHASE 4: WRAP-UP (task complete)                                       │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ skill:knowledge-boundary (final update)                           │  │
│  │ skill:signal-register (final confidence + summary)               │  │
│  │                                                                    │  │
│  │ Move inferred → known (if verified)                              │  │
│  │ Move assumed → inferred or known (if validated or confirmed)     │  │
│  │ Emit final confidence score                                       │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Calling Order (Enforced)

| # | Skill | When | Read | Write |
|---|-------|------|------|-------|
| 1 | `knowledge-boundary` | Task BEGIN | `knowledge-boundary.yaml` | `knowledge-boundary.yaml` |
| 2 | `pre-decision-check` | Task BEGIN + CHECKPOINT | `decision-guardrails.yaml` + `signal-register.yaml` | `decision-guardrails.yaml` |
| 3 | `signal-register` | After every meaningful action | `signal-register.yaml` | `signal-register.yaml` |
| 4 | `exploration-journal` | After every explore/tried/decided/learned | `exploration-journal.yaml` | `exploration-journal.yaml` |

### Data Flow Between Skills

```
knowledge-boundary.yaml
       │
       ├──→ pre-decision-check (for scope/signal queries)
       │         │
       │         └──→ signal-register.yaml (blockers → signal blockers)
       │                   │
       │                   └──→ pre-decision-check (confidence check)
       │
       └──→ exploration-journal.yaml (known items vs journal findings)
                 │
                 └──→ knowledge-boundary.yaml (journal findings → new known)
```

### Integration with SDD Skills

SDD skills MUST activate self-awareness at these points:

| SDD Skill | Activation Point | Skills to Call |
|-----------|-----------------|----------------|
| `sdd-orchestrator` | Entry + each state transition | knowledge-boundary, pre-decision-check, signal-register |
| `spec-architect` | Entry | knowledge-boundary, pre-decision-check |
| `spec-to-codebase` | Entry + each file generated | signal-register |
| `spec-contract-diff` | Entry + each diff found | signal-register, exploration-journal |
| `spec-driven-test` | Entry + each test created | signal-register |
| `spec-traceability` | Any state change | knowledge-boundary, signal-register |
| `sdd-release-guard` | Final gate | pre-decision-check (final), signal-register (final summary) |

### Integration with Vibe Skills

Vibe skills MUST activate self-awareness at these points:

| Vibe Skill | Activation Point | Skills to Call |
|------------|-----------------|----------------|
| `vibe-think` | Entry | knowledge-boundary, exploration-journal |
| `vibe-architect` | Entry + each tech decision | knowledge-boundary, pre-decision-check, signal-register |
| `vibe-design` | Entry | knowledge-boundary, pre-decision-check |
| `vibe-debug` | Entry + each attempted fix | knowledge-boundary, exploration-journal, signal-register |
| `vibe-qa` | Entry | signal-register |
| `vibe-redesign` | Entry | knowledge-boundary (verify assumptions about user intent) |
| `adaptive-planning` | Entry + scope change | knowledge-boundary, pre-decision-check, signal-register |

### Confidence Check Trigger Points

Calculate confidence AFTER adding signals. Check at these milestones:

1. **After Phase 1 (BEGIN)** — ensure task is viable
2. **After every 3-5 signals** — prevent drift
3. **Before any state promotion** (SPEC→SDD, SDD gate pass)
4. **After completing a skill** — before handing off
5. **Before asking human** — document current state first

### What NOT to Do

| Forbidden | Instead |
|-----------|---------|
| Skip knowledge-boundary when unfamiliar with domain | Stop, query, categorize |
| Proceed when confidence < 0.4 | Pause, resolve blockers |
| Continue when blockers >= 2 | STOP, ask human |
| Record vague signals like "progress" | Record specific evidence |
| Skip pre-decision-check before major decisions | Always check |
| Leave assumed items unverified indefinitely | Either verify or mark as warning |

---

## Multi-Agent Scenarios

### Scenario 1: Sequential Agents (Recommended)

```
Agent A (design): Completes work → Pushes branch → Creates PR
Agent B (review): Reviews PR → Merges → Continues work
```

### Scenario 2: Parallel Agents (Use Caution)

```
Agent A: Working on branch feature/auth
Agent B: Working on branch feature/database
Both: Use separate branches, merge independently
```

### Scenario 3: Same Branch (Avoid if Possible)

```
⚠️ Risk: Merge conflicts in .vic-sdd/ files
⚠️ Solution: Coordinate via PR reviews, use union merge
```

---

## Conflict Resolution Workflow

When multiple agents modify the same YAML files:

1. **Git detects conflict** during merge/pull request
2. **Union merge** preserves both versions (may create duplicates)
3. **Run validation script** to detect duplicate IDs
4. **Manual resolution** required to merge similar decisions
5. **Verify** application still works with merged memory

---

## Best Practices

1. **Use Separate Branches**: Each agent gets own branch
2. **Activate Self-Awareness**: Use skills before/during/after tasks
3. **Maintain Knowledge Boundary**: Keep known/inferred/assumed/unknown up-to-date
4. **Record All Signals**: Every meaningful action = one signal
5. **Query Before Acting**: Check journal to avoid duplicate exploration

---

## Directory Structure

```
.vic-sdd/
├── SPEC-REQUIREMENTS.md    # Requirements spec
├── SPEC-ARCHITECTURE.md    # Architecture spec
├── PROJECT.md              # Project status tracking
│
├── knowledge-boundary.yaml  # AI 认知地图
├── decision-guardrails.yaml # 决策约束
├── signal-register.yaml    # 信号注册
├── exploration-journal.yaml  # 探索日志
│
├── status/
│   ├── events.yaml         # Event history
│   └── state.yaml          # Current state
├── tech/
│   └── tech-records.yaml  # Technical decisions
├── risk-zones.yaml         # Risk records
├── project.yaml            # AI quick reference
└── dependency-graph.yaml  # Module dependencies

scripts/
└── verify.sh              # 外部验证脚本
```

---

## Quick Commands

```bash
# Initialize
vic init
vic spec init

# SPEC Management
vic spec status
vic spec gate 0  # Requirements
vic spec gate 1  # Architecture
vic spec gate 2  # Code alignment
vic spec gate 3  # Test coverage
vic spec merge   # Merge to final docs

# Recording
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary DB"
vic rr --id RISK-001 --area auth --desc "JWT handling"

# Validation
vic check
vic validate

# External Verification
./scripts/verify.sh
```

---

## Skills Reference

### Self-Awareness Skills (Always Active)

| Skill | Purpose | When to Activate |
|-------|---------|------------------|
| `knowledge-boundary` | AI 自知之明：knows/infers/assumes/unknown | Task BEGIN + wrap-up |
| `pre-decision-check` | 决策前刹车：scope/quality/signals check | Task BEGIN + CHECKPOINT |
| `signal-register` | 证据链进度：positive/warnings/blockers → confidence | After every meaningful action |
| `exploration-journal` | 思考过程记忆：explore/tried/decided/learned | After every exploration/decision |

### SDD Skills (Feature Delivery)

| Skill | Purpose | State |
|-------|---------|-------|
| `sdd-orchestrator` | SDD entry point, state machine, gate enforcement | Entry of Phase 2 |
| `spec-architect` | Freezes requirements into contracts | Ideation/Explore |
| `spec-to-codebase` | Generates implementation from contracts | SpecCheckpoint |
| `spec-contract-diff` | Detects drift between spec and code | Build |
| `spec-driven-test` | Builds and enforces test gates from contracts | Build/Verify |
| `spec-traceability` | Story-to-contract-to-code-to-test mapping | Any state |
| `sdd-release-guard` | Final SDD release gates | ReleaseReady |

### Vibe Skills (Exploration & QA)

| Skill | Purpose |
|-------|---------|
| `vibe-think` | Requirements clarification, user story discovery |
| `vibe-architect` | Tech selection, architecture design, SPEC-ARCHITECTURE.md |
| `vibe-redesign` | Product redesign, scope re-evaluation |
| `vibe-design` | Design system, UI/UX specifications |
| `vibe-debug` | Systematic debugging with root cause analysis |
| `vibe-qa` | Quality assurance, verification against specs |
| `adaptive-planning` | Adaptive replanning when scope changes |

### TDD Skill (Standalone Mode)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `test-driven-development` | Red-green-refactor cycle for single-module logic | No SPEC/contracts, single file/function, internal algorithm |

**Note**: `test-driven-development` is a standalone mode — NOT part of SDD pipeline. Use SDD for cross-module work, use TDD for internal logic. In layered mode, both can coexist with clear boundary (SDD = public interfaces, TDD = internal implementation).

---

## 质量红线

违反以下任一条都是不允许的：

| 红线 | 说明 |
|------|------|
| `no_todo_in_code` | 代码里不能有 TODO/FIXME |
| `no_console_in_prod` | 生产代码不能有 console.log |
| `no_hardcoded_secrets` | 不能有硬编码密钥 |
| `tests_required` | 新功能必须有测试 |
| `spec_aligned` | 必须与 SPEC 对齐 |

---

## 信心度阈值

```
confidence = (positive - warnings×0.3 - blockers×0.5) / max_signals

> 0.7    → 🟢 HIGH   → 状态良好，继续推进
0.4-0.7  → 🟡 MODERATE → 可以继续，关注警告
< 0.4    → 🔴 LOW   → 暂停，优先解决警告和阻塞
blockers >= 2 → 🛑 STOP → 停止，等待人类
```

---

> 注：详细CLI命令参考 [VIC-CLI-GUIDE.md](./docs/VIC-CLI-GUIDE.md)
