# Unified Workflow Guide

## Overview

This guide covers the complete unified workflow for SDD orchestration, Constitution enforcement, and traceability.

## SDD State Machine

```
Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
```

### State Definitions

| State | Description |
|-------|-------------|
| Ideation | Requirements gathering |
| Explore | Architecture exploration |
| SpecCheckpoint | SPEC frozen |
| Build | Implementation |
| Verify | Testing & validation |
| ReleaseReady | Ready for release |
| Released | Deployed |

### Transition Rules

- **Forward**: Only with passed gate
- **Backward**: Allowed for corrections
- **Skip**: Not allowed

## Constitution Enforcement

### Critical Rules
- SPEC-ALIGNED: Code must match SPEC
- GATE-BEFORE-COMMIT: Gates must pass
- NO-HARDCODED-SECRETS: No secrets in code

### Enforcement Flow
1. Check rules before any action
2. Block if violation found
3. Resolve before continuing

## Traceability

### Mapping Requirements
```
User Story → SPEC Contract → Code → Tests
```

### Verification Steps
1. List all user stories
2. Verify each has SPEC
3. Verify each SPEC has code
4. Verify each code has tests

## Pre-Commit Checklist

- [ ] Constitution check passed
- [ ] Gate 0-3 passed
- [ ] Traceability verified
- [ ] No TODO/FIXME in code
- [ ] No console.log in production
