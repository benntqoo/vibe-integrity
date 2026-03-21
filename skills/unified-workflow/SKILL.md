---
name: unified-workflow
description: Orchestrates SDD workflow, enforces Constitution rules, and maintains traceability.
metadata:
  domain: governance
  version: "1.0"
  tags: [sdd, orchestration, constitution, traceability, gates, workflow]
  examples:
    - "Start a new feature delivery"
    - "Advance SDD phase"
    - "Check before commit"
    - "Verify requirements-to-code mapping"
  priority: critical
  auto_activate: false
---

# Unified Workflow

## Overview

Single controller for SDD workflow, Constitution enforcement, and traceability tracking. Manages the complete feature delivery lifecycle.

**Merged from:** constitution-check + sdd-orchestrator + spec-traceability

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Start new feature delivery | ✅ Yes |
| Advance SDD phase | ✅ Yes |
| Before git commit | ✅ Yes |
| Check requirements traceability | ✅ Yes |
| During implementation | ❌ No (use implementation) |
| Clarifying requirements | ❌ No (use spec-workflow) |

## L1: Auto-Activate Triggers

| Trigger | When |
|---------|------|
| User explicitly invokes | User asks to manage workflow |
| `vic auto start` | Starting autonomous mode |
| `vic gate check` | Checking gate compliance |
| Pre-commit | Before git commit |
| Phase advancement | Moving to next SDD phase |

## L2: How to Use

### Workflow: Feature Delivery

1. **Start Delivery**
   ```bash
   vic auto start
   ```

2. **Check Constitution**
   - Read .vic-sdd/constitution.yaml
   - Verify all rules are satisfied
   - If blockers found: resolve before continuing

3. **Manage SDD Phases**
   SDD State Machine:
   ```
   Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
   ```

4. **Gate Checks at Each Phase**
   | Phase | Gate | Check |
   |-------|------|-------|
   | Ideation | Gate 0 | Requirements completeness |
   | Explore | Gate 1 | Architecture completeness |
   | Build | Gate 2 | Code alignment |
   | Verify | Gate 3 | Test coverage |

5. **Traceability Check**
   - Verify: User Story → SPEC Contract → Code → Tests
   - Each requirement has implementation
   - Each implementation has tests

6. **End Delivery**
   ```bash
   vic auto stop
   ```

### Workflow: Pre-Commit Check

1. **Run Constitution Check**
   - Read .vic-sdd/constitution.yaml
   - Check each principle

2. **Run Gate Checks**
   ```bash
   vic gate check --blocking
   ```

3. **Fix Issues if Any**
   - Resolve blockers
   - Update SPEC if needed

### Workflow: Traceability Check

1. **Read Traceability Map**
   - User Story → SPEC Contract → Code → Tests

2. **Verify Mapping**
   - Each requirement has implementation
   - Each implementation has tests

3. **Update if Needed**
   - Add missing mappings
   - Remove orphaned code

## L3: References (Required Reading)

These references are part of the skill, not optional:

### Required (Always Read)
- `references/unified-workflow-guide.md` - Complete usage guide

### Optional (Read if Needed)
- `references/sdd-state-machine.md` - SDD state machine details
- `references/constitution-rules.md` - Constitution rule definitions
- `references/traceability-patterns.md` - Traceability patterns
