# Debugging Guide

> Systematic debugging methodology for VIBE-SDD

## Overview

This guide covers the 4-phase systematic debugging approach used in VIBE-SDD. This methodology ensures efficient root cause identification and prevents "whack-a-mole" fixes.

## 4-Phase Methodology

```
1️⃣ SURVEY → 2️⃣ PATTERN → 3️⃣ HYPOTHESIS → 4️⃣ IMPLEMENT
Gather       Find         Form &        Fix root
evidence     patterns    test          cause
```

## Phase Details

### Phase 1: SURVEY

**Purpose**: Gather comprehensive evidence before forming conclusions.

**Activities**:
1. Reproduce the issue
2. Document exact error messages
3. Record environment details (OS, versions, config)
4. Check logs and stack traces
5. Identify when the issue started (git bisect if needed)

**Vic Command**:
```bash
vic debug start --problem "Login fails in production"
vic debug survey
```

**Evidence Checklist**:
- [ ] Issue reproduced consistently
- [ ] Error message captured
- [ ] Environment documented
- [ ] Logs collected
- [ ] Timeline established

### Phase 2: PATTERN

**Purpose**: Find similar issues and known patterns.

**Activities**:
1. Search for similar issues in:
   - Issue tracker
   - Documentation
   - Codebase history
2. Check if it's a known bug
3. Look for recent changes that might have caused it
4. Identify patterns in error occurrences

**Vic Command**:
```bash
vic debug pattern
```

**Pattern Sources**:
| Source | What to Look For |
|--------|------------------|
| Git history | Recent changes to affected area |
| Issue tracker | Similar reported bugs |
| Documentation | Known limitations |
| Stack Overflow | Common solutions |
| Codebase | Similar error handling |

### Phase 3: HYPOTHESIS

**Purpose**: Form and test root cause hypothesis.

**Activities**:
1. Form a specific, testable hypothesis
2. Design an experiment to test it
3. Run the experiment
4. Document results

**Vic Command**:
```bash
vic debug hypothesis --explain "Token expires without refresh"
```

**Hypothesis Template**:
```
Hypothesis: [specific root cause]
Because: [why this makes sense]
Test: [how to verify]
Expected: [what should happen if correct]
Actual: [what actually happened]
```

**Example**:
```
Hypothesis: JWT token validation is failing due to clock skew
Because: Production server time is 5 minutes ahead
Test: Compare server timestamps
Expected: Tokens should be valid within tolerance
Actual: Tokens rejected as expired immediately
```

### Phase 4: IMPLEMENT

**Purpose**: Fix the root cause and prevent recurrence.

**Activities**:
1. Implement the fix
2. Write a regression test
3. Verify the fix works
4. Document the fix

**Vic Command**:
```bash
vic debug implement --fix "Add token refresh logic" --root-cause "Token expires without refresh"
```

**Fix Checklist**:
- [ ] Root cause addressed
- [ ] Regression test written
- [ ] Fix verified in all environments
- [ ] Documentation updated
- [ ] No new issues introduced

## ⚠️ STOP Rule

**If you fail 3 times, STOP and reconsider the approach.**

| Attempt | Action |
|---------|--------|
| 1st fail | Try different hypothesis |
| 2nd fail | Re-survey for more evidence |
| 3rd fail | **STOP** - Question the architecture |

When you reach the 3rd failed attempt:
1. Step back and re-examine assumptions
2. Consider if the architecture is fundamentally flawed
3. Ask for help or escalation
4. Document all attempts for future reference

## Debugging Checklist

### Before Starting
- [ ] Issue clearly defined
- [ ] Reproduction steps documented
- [ ] Environment details recorded

### During Investigation
- [ ] Evidence gathered systematically
- [ ] Similar issues researched
- [ ] Hypothesis formed and tested

### After Fix
- [ ] Root cause confirmed
- [ ] Regression test added
- [ ] Fix verified in all environments
- [ ] Documentation updated

## Common Bug Categories

| Category | Typical Causes | Debug Approach |
|----------|----------------|----------------|
| **Logic** | Wrong conditions, edge cases | Check assumptions, add logging |
| **Data** | Null values, type mismatches | Validate inputs, check boundaries |
| **Integration** | API changes, version mismatch | Check contracts, verify versions |
| **Performance** | N+1 queries, memory leaks | Profile, check resource usage |
| **Environment** | Config differences, secrets | Compare environments, check config |

## Tools

### Logging
```javascript
// Add strategic logging
console.log('[DEBUG] Input:', JSON.stringify(input));
console.log('[DEBUG] Output:', JSON.stringify(result));
```

### Git Bisect
```bash
# Find when bug was introduced
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git will guide you through binary search
```

### Diff Check
```bash
# Check recent changes
git diff HEAD~10..HEAD -- path/to/affected/file
```

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| "Try random fixes" | No understanding of root cause | Follow SURVEY → HYPOTHESIS |
| "It works on my machine" | Ignores environment differences | Document and compare environments |
| "Just restart the server" | Masks underlying issue | Investigate root cause |
| "Add more logging" without purpose | Noise without insight | Add strategic logging with hypothesis |
| "Copy Stack Overflow solution" | May not apply to your context | Understand before applying |

## Integration with SDD

| SDD Phase | Debug Action |
|----------|--------------|
| Build | Use Phase 1-4 debugging |
| Verify | Run regression tests |
| ReleaseReady | Document fix in changelog |

## Summary

| Phase | Duration | Key Output |
|-------|----------|------------|
| SURVEY | 30% of time | Evidence document |
| PATTERN | 20% of time | Related issues list |
| HYPOTHESIS | 30% of time | Tested hypothesis |
| IMPLEMENT | 20% of time | Working fix + test |

**Remember**: The goal is to fix the **root cause**, not just the symptoms. If you don't understand why it broke, you haven't fixed it.
