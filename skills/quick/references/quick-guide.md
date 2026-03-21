# Quick Workflow Guide

## Overview

This guide helps determine if a task qualifies as "quick" and how to handle it.

## Quick Task Criteria

A task is "quick" if ALL of:
- [ ] Single file affected
- [ ] No SPEC impact
- [ ] No complex logic
- [ ] No test changes needed
- [ ] No dependency changes
- [ ] < 10 lines changed

## Examples

### ✅ Quick Tasks
- Fix typo in README
- Rename variable (single file)
- Add inline comment
- Format code
- Update import order

### ❌ NOT Quick Tasks
- Multi-file refactor
- API changes
- Database migrations
- New feature implementation
- Bug fix with tests

## Workflow

### Step 1: Verify Quick
1. Confirm single file
2. Estimate < 10 lines
3. Check no SPEC impact

### Step 2: Make Change
1. Edit only necessary lines
2. No refactoring
3. Minimal change

### Step 3: Verify
1. Run diagnostics
2. Ensure clean build
3. Commit

## Escalation Decision

```
Is it quick?
├─ Yes → Use quick skill
└─ No → Which category?
    ├─ Requirements/Architecture → spec-workflow
    ├─ Implementation/Testing → implementation
    └─ Workflow/Process → unified-workflow
```

## Anti-Patterns

| Anti-Pattern | Problem |
|--------------|---------|
| "Just a quick rename" | Becomes multi-file change |
| "Just a quick comment" | Changes behavior |
| "Just a quick fix" | Requires tests |
