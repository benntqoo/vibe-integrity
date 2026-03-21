# Blocker Types Reference

## Complete Blocker List

### spec_unaligned
- **Meaning**: Code vs SPEC mismatch
- **Severity**: 🔴 Blocker
- **Required Action**: 
  1. Run `vic spec diff` to see changes
  2. Choose: Update SPEC or fix code
  3. Re-run constitution-check

### unknown_blocking
- **Meaning**: Unknown issue blocking progress
- **Severity**: 🔴 Blocker
- **Required Action**:
  1. Document specific issue
  2. Ask human for clarification
  3. Don't guess and continue

### decision_blocking
- **Meaning**: Need decision to continue
- **Severity**: 🟡 High
- **Required Action**:
  1. List all options
  2. Analyze pros/cons
  3. Request decision

### env_blocking
- **Meaning**: Environment issue
- **Severity**: 🟡 High
- **Required Action**:
  1. Diagnose environment issue
  2. Fix environment
  3. Verify fix

## Blocker Resolution Flow

```
Detect blocker
    ↓
Classify blocker type
    ↓
Execute corresponding action
    ↓
Verify resolution
    ↓
Recalculate confidence
    ↓
confidence >= 0.4? ──No──→ Continue resolving
    ↓Yes
Continue work
```
