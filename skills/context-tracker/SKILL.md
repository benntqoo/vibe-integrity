# Context Tracker Skill

## Overview

Consolidated self-awareness skill combining:
- knowledge-boundary
- pre-decision-check  
- signal-register
- exploration-journal

## Single File: `.vic-sdd/context.yaml`

```yaml
# Context Tracking - Single Source of Truth
# =========================================

known:      # Verified facts (highest confidence)
  - "vic CLI is Go-based"
  - "SPEC files are markdown"

inferred:   # Inferred from patterns (needs verification)
  - "User wants CLI tool improvements"

assumed:    # Assumptions (high risk, verify soon)
  - "CLI is primary interface"

unknown:    # Knowledge gaps (blockers)
  - []

signals:
  positive: []
  warnings: []
  blockers: []

confidence: 1.0  # Calculated: (positive - warnings*0.3 - blockers*0.5) / max_signals

exploration:
  entries:
    - action: explore
      topic: "current project structure"
      timestamp: "2026-03-19"
    - action: decided
      topic: "consolidate skills to 10"
      alternatives: ["keep 19", "merge to 7", "merge to 10"]
      choice: "merge to 10"
      reason: "balance between simplicity and coverage"
```

## When to Use

### Task BEGIN

```markdown
1. Read .vic-sdd/context.yaml
2. Update known/inferred/assumed/unknown for current task
3. Calculate confidence
4. If blockers >= 2 → STOP, ask human
5. If confidence < 0.4 → pause, resolve blockers
```

### After Every Meaningful Action

```markdown
1. Signal register: Record positive/warning/blocker
2. Recalculate confidence
3. Update exploration journal
```

### Task END (Wrap-up)

```markdown
1. Move inferred → known (if verified)
2. Move assumed → inferred/known (if validated)
3. Emit final confidence score
```

## Confidence Thresholds

```
> 0.7    → 🟢 HIGH   → Continue
0.4-0.7  → 🟡 MODERATE → Continue, monitor warnings
< 0.4    → 🔴 LOW   → Pause, resolve blockers
blockers >= 2 → 🛑 STOP → Ask human
```

## Quick Reference

| Action | What to Record |
|--------|---------------|
| explored | What you discovered |
| tried | Methods that worked/failed |
| decided | Choice + alternatives + reason |
| learned | Lessons to remember |

## File Location

`.vic-sdd/context.yaml`
