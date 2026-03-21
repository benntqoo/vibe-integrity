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
