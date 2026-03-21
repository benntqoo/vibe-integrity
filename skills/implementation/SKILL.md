---
name: implementation
description: Handles code implementation, debugging, testing, and SPEC alignment.
metadata:
  domain: engineering
  version: "1.0"
  tags: [implementation, debugging, testing, coding, tdd]
  examples:
    - "Implement a new feature"
    - "Fix a bug"
    - "Write tests for code"
    - "Check code vs SPEC alignment"
  priority: critical
  auto_activate: false
---

# Implementation Workflow

## Overview

Handles the complete implementation lifecycle from coding to testing to SPEC alignment. Includes systematic debugging and TDD workflow.

**Merged from:** debugging + qa + spec-contract-diff

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Implementing new feature | ✅ Yes |
| Fixing a bug | ✅ Yes |
| Writing or running tests | ✅ Yes |
| Checking code vs SPEC alignment | ✅ Yes |
| Designing system architecture | ❌ No (use spec-workflow) |
| Clarifying requirements | ❌ No (use spec-workflow) |

## L1: Auto-Activate Triggers

| Trigger | When |
|---------|------|
| User explicitly invokes | User asks to implement, fix, or test |
| `implement`, `code`, `fix`, `debug` mentioned | Task involves coding |
| Test coverage | User asks to check or improve test coverage |
| SPEC alignment | `vic spec gate 2` or `vic check` called |

## L2: How to Use

### Option A: Feature Implementation (TDD)

1. **Read SPEC**
   - Read SPEC-ARCHITECTURE.md
   - Read SPEC-REQUIREMENTS.md

2. **Start TDD**
   ```bash
   vic tdd start --feature "[feature]"
   ```

3. **RED Phase**: Write failing test
   ```bash
   vic tdd red --test "[test description]"
   ```

4. **GREEN Phase**: Make it pass
   ```bash
   vic tdd green --test "[test description]" --passed
   ```

5. **REFACTOR Phase**: Improve code
   ```bash
   vic tdd refactor
   ```

6. **Check Alignment**
   - Run `vic spec gate 2`
   - If failed: Fix alignment

7. **Check Tests**
   - Run `vic spec gate 3`
   - If failed: Fix tests

### Option B: Bug Fix (Systematic Debugging)

1. **Start Debug Session**
   ```bash
   vic debug start --problem "[description]"
   ```

2. **Survey**: Gather evidence
   ```bash
   vic debug survey
   ```

3. **Pattern**: Find similar issues
   ```bash
   vic debug pattern
   ```

4. **Hypothesis**: Form and test
   ```bash
   vic debug hypothesis --explain "[explanation]"
   ```

5. **Implement**: Fix root cause
   ```bash
   vic debug implement --fix "[fix description]" --root-cause "[root cause]"
   ```

6. **Verify**: Run tests to confirm fix

### Option C: SPEC Alignment Check

1. **Run Gate 2**
   ```bash
   vic spec gate 2
   ```

2. **If failed**:
   - Option A: Update SPEC (preferred)
   - Option B: Fix code alignment

## L3: References (Required Reading)

These references are part of the skill, not optional:

### Required (Always Read)
- `references/implementation-guide.md` - Complete usage guide

### Optional (Read if Needed)
- `references/tdd-guide.md` - TDD workflow details
- `references/debugging-guide.md` - Systematic debugging methodology
- `references/troubleshooting.md` - Common issues and fixes
