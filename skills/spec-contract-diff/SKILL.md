---
name: spec-contract-diff
description: Use when implementation exists at Build state and you need to detect drift between actual code interfaces and spec contracts.
---

# Spec Contract Diff

## Overview
Prevents silent contract drift by comparing spec contracts with actual public interfaces. Ensures implemented code matches defined contracts.

## When to Use

**Use when:**
- Current state is Build
- Implementation code exists
- Need to verify code matches contract specifications
- Detecting unintended API changes

**When NOT to use:**
- No implementation yet (use spec-to-codebase)
- Contract itself needs updates (return to spec-architect)

## Invocation Alignment

- If `sdd-orchestrator` is present, it is the only state-transition entry
- Direct invocation is limited to read-only diff analysis
- Direct invocation must not promote state; control returns to `sdd-orchestrator`

## Entry Conditions (All Must Be True)

1. Current state is `Build`
2. `.sdd-spec/specs/<feature>.contract.json` exists

## Comparison Scope

Check all externally visible surfaces:
- API routes
- Service method signatures
- Event payload schemas
- Error codes and error payload shapes

## Quick Reference

| Gate Check | Pass Condition |
|------------|----------------|
| Removed Operations | Must have breaking-change declaration |
| Required Fields | Cannot be removed from output contracts |
| Error Codes | Must remain compatible |
| Compatibility | Result must be pass |

## Required Outputs

- `.sdd-spec/specs/<feature>.contract.diff.json`

**Required fields:**
- feature, state_before, state_after, skill, timestamp
- result, blocking_reasons
- added_operations, removed_operations
- signature_mismatches, error_contract_mismatches
- compatibility_result, requires_spec_update

## Failure Policy

**On failure:**
- Mark `requires_spec_update` as true
- Block transition to Verify
- Route control back to spec-architect

## Success Policy

**On success:**
- Keep or promote state to Build
- Allow invocation of spec-driven-test

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring signature changes | Check all method signatures, not just additions |
| Missing error code changes | Verify error codes remain backward compatible |
| Approving without full check | Validate all comparison scope items |
| Silently allowing drift | Always set requires_spec_update when drift detected |

## Machine Contracts

Report structure must conform to `skills/sdd-orchestrator/sdd-machine-schema.json`.
Gate checklist defined in `skills/sdd-orchestrator/sdd-gate-checklist.json`.

---

## Pipeline Metadata

pipeline_metadata:
  handoff:
    delivers:
      - artifact: ".sdd-spec/specs/<feature>.contract.diff.json"
        description: "Diff report with added/removed operations, signature mismatches"
    consumes:
      - artifact: ".sdd-spec/specs/<feature>.contract.json"
        description: "Expected contract"
      - artifact: "implementation code"
        description: "Actual code interfaces"
  exit_condition:
    success: "No drift detected, requires_spec_update=false"
    failure: "Drift detected, requires_spec_update=true"
    triggers_next_on_success: "spec-driven-test (stay in Build)"
    triggers_next_on_failure: "spec-architect (requires_spec_update=true, return to Explore)"
  agent_pattern: Reviewer