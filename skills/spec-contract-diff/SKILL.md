---
name: "spec-contract-diff"
description: "Detects drift between implemented interfaces and spec contracts. Invoke after code generation and before contract tests."
---

# Spec Contract Diff

Prevents silent contract drift by comparing spec contracts and actual public interfaces.

All conditions must be true:
- Current state is `CodeGenerated` or `Implemented`
- `.sdd-spec/specs/<feature>.contract.json` exists

- Current state is `CodeGenerated` or `Implemented`
- `docs/specs/<feature>.contract.json` exists

## Invocation Alignment

- If `sdd-orchestrator` is present, it is the only state-transition entry
- Direct invocation is limited to read-only diff analysis
- Direct invocation must not promote state; control returns to `sdd-orchestrator`

## Outputs

Generate:
- `.sdd-spec/specs/<feature>.contract.diff.json`

Generate:
- `docs/specs/<feature>.contract.diff.json`

Required fields:
- `feature`
- `state_before`
- `state_after`
- `skill`
- `timestamp`
- `result`
- `blocking_reasons`
- `added_operations`
- `removed_operations`
- `signature_mismatches`
- `error_contract_mismatches`
- `compatibility_result`
- `requires_spec_update`

Report structure must conform to `skills/sdd-orchestrator/sdd-machine-schema.json`.

## Comparison Scope

Check all externally visible surfaces declared in spec:
- API routes
- Service method signatures
- Event payload schemas
- Error codes and error payload shapes

## Gate Rules

Pass only when:
- No removed operation without breaking-change declaration
- No required field removed from output contracts
- Error codes remain compatible
- `compatibility_result` is `pass`
- All checklist items for `spec-contract-diff` pass in `skills/sdd-orchestrator/sdd-gate-checklist.json`

## Failure Policy

On failure:
- Mark `requires_spec_update` as true
- Block transition to `ContractVerified`
- Route control back to `spec-architect` for contract correction

## Success Policy

On success:
- Keep or promote state to `Implemented`
- Allow invocation of `spec-driven-test`
