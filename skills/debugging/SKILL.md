# Debugging Skill

## Overview

Combines vibe-debug + adaptive-planning for systematic debugging.

**When to use:**
- Bug in production or tests
- Unexpected behavior
- Root cause unclear

## Process: SURVEY → PATTERN → HYPOTHESIS → IMPLEMENT

### Phase 1: SURVEY - Gather Evidence

```bash
# Document the problem
echo "Problem: [describe]"
echo "When: [trigger conditions]"
echo "Expected: [what should happen]"
echo "Actual: [what happened]"
```

Check:
- Error messages
- Stack traces
- Logs
- Recent changes

### Phase 2: PATTERN - Find Similar Issues

Search codebase for:
- Similar error handling patterns
- Related modules
- Recent changes that might have caused it

### Phase 3: HYPOTHESIS - Form and Test

```
Hypothesis: [root cause explanation]
Test: [how to verify]
If [test passes], then [hypothesis confirmed]
If [test fails], then [back to SURVEY]
```

### Phase 4: IMPLEMENT - Fix Root Cause

```
Fix: [what you changed]
Root Cause: [why it broke]
Prevention: [how to prevent recurrence]
```

## Stopping Rule

⚠️ **STOP after 3 failed attempts**
- Question the architecture itself
- Ask for human help
- Do NOT continue patching

## Update Context

After fixing, update `.vic-sdd/context.yaml`:
```yaml
known:
  - "Found root cause: missing error handling"
  - "Fixed by adding nil check"
exploration:
  entries:
    - action: decided
      topic: "error handling approach"
      alternatives: ["add nil check", "use error wrapper", "panic"]
      choice: "add nil check"
      reason: "minimal change, clear intent"
```

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `context-tracker` | Update context after debugging |
| `qa` | Write test to prevent regression |
