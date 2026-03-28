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

| Situation | Use Skill? |
|-----------|------------|
| Task BEGIN | ✅ Yes |
| After every action | ✅ Yes |
| After decisions | ✅ Yes |
| Task END | ✅ Yes |
| Simple code changes | ❌ No |

## L1: Auto-Activate Triggers

| Trigger | When |
|---------|------|
| User explicitly invokes | User asks to check context or confidence |
| `context-tracker` mentioned | User mentions knowledge, confidence, or blockers |
| Task BEGIN | Starting new task |
| After major actions | After completing significant work |

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
  blockers: []     # spec_unaligned, unknown_blocking
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

## Next Skill Guidance

After context-tracker assessment, choose the next skill based on current state:

### Decision Matrix

| Current State | Confidence | Recommended Next Skill | Reason |
|---------------|------------|----------------------|--------|
| Requirements vague | Any | `spec-workflow` | Need to clarify and freeze requirements |
| SPEC not created | Any | `spec-workflow` | Must create SPEC before implementation |
| SPEC frozen, Ready to code | HIGH | `implementation` | Clear requirements, can proceed |
| Bug reported | Any | `implementation` | Use systematic debugging |
| Code complete | MODERATE+ | `implementation` | Run Gate 2/3 checks |
| Ready to commit | HIGH | `unified-workflow` | Pre-commit gate checks |
| Simple single-file change | HIGH | `quick` | Low-risk, no SPEC impact |
| Multiple blockers | Any | Ask human | Cannot proceed automatically |

### Quick Decision Flowchart

```
Context Updated
    │
    ├─ Has blockers? ── Yes ──→ 🛑 Resolve blockers first
    │                              or Ask human
    │
    └─ No blockers
        │
        ├─ Confidence HIGH?
        │   ├─ Yes ── Requirements clear? ── Yes ──> implementation
        │   │                      │
        │   │                      └─ No ──> spec-workflow
        │   │
        │   └─ No ── Confidence MODERATE?
        │              │
        │              ├─ Yes ── Monitor warnings, May proceed
        │              │
        │              └─ No ── 🛑 Pause. Build confidence first
        │
        └─ Task type?
            ├─ Simple change ──> quick
            ├─ Commit needed ──> unified-workflow
            └─ Complex task ──> See matrix above
```

## Intelligent Assessment

Automatic task analysis for zero-decision workflow. The system detects change type, assesses risk, and selects appropriate workflow automatically.

### Step 1: Detect Change Type

| Change Type | Indicators | Risk | Auto-Skill |
|-------------|------------|------|------------|
| `typo_fix` | files≤1, lines<10, no logic change | Minimal | `quick` |
| `rename_refactor` | files≤5, rename only, no logic change | Low | `quick` |
| `bug_fix` | keywords: fix/bug/error, test added | Medium | `implementation` |
| `feature_addition` | keywords: feat/add/new, new functions | High | `implementation` |
| `architecture_change` | files>10, SPEC affected, refactor keywords | Critical | `spec-workflow` |

**Detection Methods:**
```bash
# Analyze git diff
git diff --stat
git diff --name-only

# Check SPEC impact
git diff --name-only | grep -E "SPEC-.*\.md|\.vic-sdd/"
```

[参考: references/change-detection.md]

### Step 2: Assess Risk Level

**Risk Formula:**
```
risk_score = (scope + complexity + spec_impact + test_coverage) / 4
```

**Factor Scoring:**

| Factor | Score 1 | Score 2 | Score 3 | Score 4 |
|--------|---------|---------|---------|---------|
| Scope | single file | single module | multi modules | cross-cutting |
| Complexity | trivial | simple | moderate | complex |
| SPEC Impact | none | minor | moderate | major |
| Test Coverage | existing sufficient | needs update | needs new | needs integration |

**Risk Levels:**

| Level | Score | Gates Required | Workflow |
|-------|-------|----------------|----------|
| Minimal | 0.0-0.5 | None | `quick` |
| Low | 0.5-1.5 | gate_2 | `quick` |
| Medium | 1.5-2.5 | gate_2, gate_3 | `implementation` |
| High | 2.5-3.5 | gate_0, gate_2, gate_3 | `implementation` |
| Critical | 3.5-4.0 | All gates | `spec-workflow` → `implementation` |

[参考: references/risk-assessment.md]

### Step 3: Auto-Transition

Automatic skill switching without user decision:

| Condition | From | To | Notify |
|-----------|------|-----|--------|
| Requirements vague / SPEC missing | any | `spec-workflow` | "需求不清晰，自动切换" |
| SPEC frozen + confidence≥0.7 | `spec-workflow` | `implementation` | "SPEC 已冻结，开始实现" |
| Code complete + gates passed | `implementation` | `unified-workflow` | "准备提交检查" |
| Risk minimal/low | any | `quick` | "简单变更，快速通道" |

### Quick Assessment Command

```bash
# One-command assessment
vic assess

# Output example:
# Change Type: bug_fix
# Risk Level: medium (2.1)
# Gates Required: [gate_2, gate_3]
# Recommended Skill: implementation
# Auto-switch: yes
```

## Vic Commands

| Scenario | Command | When to Use |
|----------|---------|-------------|
| **Intelligent assessment** | `vic assess` | Automatic task analysis |
| Session start | `vic status` | Read overall project status |
| Session start | `vic spec status` | Check current SPEC document status |
| Session start | `vic spec hash` | Detect if SPEC has changed since last session |
| Session start | `vic gate check --blocking` | Check all Gate blocking issues |
| Confidence assessment | `vic cost status` | View token consumption, assess session cost |
| Dependency overview | `vic deps list` | Understand module structure (impact scope) |
| After context update | `vic history --limit 5` | View recent events, confirm context continuity |

## L3: References

- references/
  - `context-tracker-guide.md` - Complete usage guide
  - `blocker-types.md` - Blocker type definitions
  - `confidence-formula.md` - Confidence calculation formula
  - `change-detection.md` - Change type detection algorithm
  - `risk-assessment.md` - Risk level evaluation matrix
