# VIBE-SDD Agent Collaboration Guide

> **AI 入口文件** — 此文件定义 AI 进入项目时的起点。
> **详细执行步骤和 vic 命令调用 → 见各 SKILL.md**

---

## 系统状态

| Feature | Status |
|---------|--------|
| Structured Development | ✅ .vic-sdd/ SPEC workflow |
| AI Self-Awareness | ✅ context-tracker (auto_activate) |
| Gate Checks | ✅ vic spec gate 0-3 |
| Constitution Rules | ✅ constitution.yaml |
| Skills System | ✅ 5 Skills (Google Cloud Agent Skills spec) |

---

## Skills Overview (5 Core Skills)

| Skill | When to Activate | Responsibility |
|-------|-----------------|----------------|
| **`context-tracker`** | **Every session start + after each action + session end** | AI self-awareness, confidence tracking, blocker identification |
| **`spec-workflow`** | Vague requirements / architecture design / SPEC creation | Requirements analysis → architecture design → SPEC freezing |
| **`implementation`** | Code implementation / bug fix / testing / SPEC alignment | TDD red-green-refactor, systematic debugging, Gate 2/3 checks |
| **`unified-workflow`** | Feature delivery / phase advancement / pre-commit / traceability | SDD state machine, constitution enforcement, traceability |
| **`quick`** | Simple single-file changes (no SPEC impact) | Typo fixes, variable renaming, simple comments |

---

## Decision Tree: Which Skill to Use?

```
AI enters project → confirm context → execute work → wrap up

Step 1: Confirm context (context-tracker, auto_activate)
  → vic status
  → vic spec status
  → vic spec hash
  → vic gate check --blocking
  → Check .vic-sdd/ state files
  (details → skills/context-tracker/SKILL.md)

Step 2: Determine task type
  │
  ├─ 🤔 Vague requirements / undesign architecture / need SPEC
  │   └─→ spec-workflow
  │       (details → skills/spec-workflow/SKILL.md)
  │
  ├─ 💻 Code implementation / bug fix / write tests / check alignment
  │   └─→ implementation
  │       (details → skills/implementation/SKILL.md)
  │
  ├─ 🚀 Feature delivery / phase advancement / pre-commit / traceability
  │   └─→ unified-workflow
  │       (details → skills/unified-workflow/SKILL.md)
  │
  └─ 🔧 Simple changes (single file, no SPEC impact)
      └─→ quick
          (details → skills/quick/SKILL.md)
```

---

## Pre-work Commands (Project startup / planning requirements)

> **These commands should be run before any substantive work begins.**
> **Detailed command descriptions and parameters → each SKILL.md**

### Session Start (First thing in every conversation)

```bash
vic status                              # Overall project status
vic spec status                         # SPEC document status
vic spec hash                           # Check if SPEC has changed
vic gate check --blocking               # All Gate status (blocking issues)
```

### Planning Phase (Before starting design or requirement clarification)

```bash
vic spec list                           # List all SPEC documents
vic spec show                           # Show SPEC summary
vic milestone list                       # Project milestones
vic task list                           # Remaining tasks (if any)
```

### Status Query (Available anytime)

```bash
vic history --limit 10                  # Recent events
vic search <keyword>                     # Search technical decisions and risks
vic deps list                           # Module dependency overview
vic cost status                         # Token/cost tracking
```

---

## SDD State Machine

```
Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
    │         │            │             │        │          │            │
    ▼         ▼            ▼             ▼        ▼          ▼            ▼
spec-workflow                   implementation              unified-workflow
                               (Gate 2: Code alignment)      (Gate 3: Test coverage)
                               (Gate 3: Test coverage)      (Final delivery check)
```

---

## Quality Rules (Must Not Violate)

See `skills/context-tracker/SKILL.md` and `.vic-sdd/constitution.yaml`

| Rule ID | Description | Trigger |
|---------|-------------|---------|
| `SPEC-FIRST` | Must change SPEC before changing code | implementation |
| `SPEC-ALIGNED` | Code must align with SPEC | Gate 2 |
| `NO-TODO-IN-CODE` | Code禁止 TODO/FIXME | Gate 0 |
| `NO-CONSOLE-IN-PROD` | No console.log in production code | Pre-commit |
| `GATE-BEFORE-COMMIT` | Must pass Gates before commit | unified-workflow |
| `TESTS-REQUIRED` | New features must have tests | implementation |
| `SELF-AWARENESS` | Update context after each action | context-tracker |

---

## Confidence (Automatically calculated by context-tracker)

```
confidence = (positive - warnings×0.3 - blockers×0.5) / max_signals

> 0.7    → 🟢 HIGH   → Continue
0.4-0.7  → 🟡 MODERATE → Continue, monitor warnings
< 0.4    → 🔴 LOW   → Pause, resolve blockers
blockers >= 2 → 🛑 STOP → Stop, ask human
```

---

## Directory Structure (AI Must-Read Files)

```
.vic-sdd/
├── SPEC-REQUIREMENTS.md    # Requirements spec (read first)
├── SPEC-ARCHITECTURE.md    # Architecture spec (read first)
├── PROJECT.md               # Project status tracking
├── constitution.yaml        # Unbreakable rules (read first)
├── context.yaml            # AI self-awareness state (maintained by context-tracker)
├── agent-prompt.md         # AI workflow prompt (with mandatory checklists)
└── status/
    └── spec-hash.json      # Change detection

skills/
├── context-tracker/        # AI self-awareness (auto_activate: true)
├── spec-workflow/          # Requirements/architecture/SPEC creation
├── implementation/          # Code/debugging/testing/alignment
├── unified-workflow/        # SDD orchestration/constitution/traceability
└── quick/                 # Simple single-file changes
```

---

## Detailed Documentation Index

| Scenario | Document |
|----------|----------|
| Who I am / What I should do | AGENTS.md (this file) |
| How to update status after each action | skills/context-tracker/SKILL.md |
| Vague requirements, architecture design, SPEC creation | skills/spec-workflow/SKILL.md |
| Write code, fix bugs, tests, SPEC alignment | skills/implementation/SKILL.md |
| Feature delivery, phase advancement, constitution, traceability | skills/unified-workflow/SKILL.md |
| Simple single-file changes | skills/quick/SKILL.md |
| CLI tool complete command reference | docs/VIC-CLI-GUIDE.md |

---

> **Core Principle**: AGENTS.md is the AI's "entry map" - keep it simple.
> Detailed work steps, vic command chains, specific parameters → loaded when corresponding Skill is activated.
> This prevents context explosion while ensuring every execution step is documented.
