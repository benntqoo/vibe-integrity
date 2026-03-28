---
name: quick
description: Handles simple, single-file changes that don't require full SDD workflow.
metadata:
  domain: engineering
  version: "1.0"
  tags: [quick, simple, single-file, trivial, typo, rename]
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

**This skill is for low-risk, simple changes only.**

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Fix a typo | ✅ Yes |
| Rename a variable | ✅ Yes |
| Add comments | ✅ Yes |
| Simple single-file refactor | ✅ Yes |
| Multi-file changes | ❌ No (use implementation) |
| New feature | ❌ No (use spec-workflow) |
| Complex bug fix | ❌ No (use implementation) |
| Architecture changes | ❌ No (use spec-workflow) |

## L1: Auto-Activate Triggers

| Trigger | When |
|---------|------|
| User explicitly invokes | User asks for simple change |
| `quick`, `typo`, `rename` mentioned | Task described as simple |
| Single file scope | Only one file affected |

**Escalation triggers** (when to NOT use this skill):

### Quantified Escalation Criteria

| Metric | Quick Threshold | If Exceeded → Escalate To |
|--------|-----------------|--------------------------|
| Files changed | ≤ 1 file | `implementation` |
| Lines changed | ≤ 50 lines | `implementation` |
| Functions modified | ≤ 2 functions | `implementation` |
| Nesting depth change | ≤ 1 level | `implementation` |
| SPEC files affected | 0 files | `spec-workflow` |
| Test files needed | No new tests | `implementation` |
| New dependencies | None | `spec-workflow` |

### Automatic Escalation Detection

```bash
# Check file count
git diff --name-only | wc -l
# If > 1, escalate to implementation

# Check line count
git diff --stat | grep -oE '[0-9]+ insertion' | head -1
# If > 50 insertions, escalate to implementation

# Check SPEC impact
git diff --name-only | grep -E "SPEC-.*\.md|\.vic-sdd/"
# If any match, escalate to spec-workflow
```

### Decision Flowchart

```
Change Detected
    │
    ├─ Files > 1? ─────── Yes ──→ implementation
    │
    ├─ Lines > 50? ────── Yes ──→ implementation
    │
    ├─ SPEC affected? ──── Yes ──→ spec-workflow
    │
    ├─ Tests needed? ───── Yes ──→ implementation
    │
    └─ All checks pass ────→ ✅ Continue quick
```

## L2: How to Use

### Step 1: Verify Scope

1. **Confirm Single File**
   - Only one file affected
   - No SPEC impact

2. **Confirm Simplicity**
   - No complex logic changes
   - No test changes needed
   - No dependency changes

### Step 2: Make Change

1. **Edit File**
   - Make the minimal change
   - Don't add unnecessary changes

2. **Run Diagnostics**
   - Check for LSP errors
   - Fix any issues

### Step 3: Quick Verification

1. **Build if applicable**
   - Ensure code compiles

2. **Commit if clean**
   - Simple commit message
   - Example: "fix: typo in README.md"

### When to Escalate

If the change turns out to be more complex:
- Multi-file changes → use `implementation` skill
- SPEC impact → use `spec-workflow` skill
- Complex logic → use `implementation` skill

## Vic Commands

| Scenario | Command | When to Use |
|----------|---------|-------------|
| Confirm single file | `vic deps list` | Verify changes only affect single module |
| AI Slop check | `vic slop scan --type code` | Scan for AI Slop code patterns after changes |
| AI Slop fix | `vic slop fix --dry-run=false` | Apply automatic fixes (preview before execution) |
| Diagnostic check | `vic check --category <category>` | Confirm changes don't affect tech stack decisions |
| Status confirmation | `vic status` | Confirm overall project status is normal |

## L3: References

- references/
  - `quick-guide.md` - Complete usage guide
  - `examples.md` - Examples of quick vs non-quick tasks
  - `escalation.md` - Escalation criteria
