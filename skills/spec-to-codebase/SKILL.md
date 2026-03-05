---
name: "spec-to-codebase"
description: "Generates implementation from validated spec contracts. Invoke only after SpecValidated and before implementation diverges."
---

# Spec-to-Codebase

Builds deterministic code changes from spec artifacts and enforces contract-preserving generation.

## Mandatory Entry Conditions

All conditions must be true:
- Current state is `SpecValidated`
- `docs/specs/<feature>.contract.json` exists
- `breaking_change` policy in contract is explicit
- Traceability file exists and contains story IDs

If any condition fails, stop and return to `spec-architect`.

## Invocation Alignment

- If `sdd-orchestrator` is present, it is the only state-transition entry
- Direct invocation is limited to read-only analysis or generation planning
- Direct invocation must not promote state; control returns to `sdd-orchestrator`

## State Transition Contract

- Input state: `SpecValidated`
- Output state on success: `CodeGenerated`
- Output state on failure: `SpecValidated`

## Generation Rules

1. Read these inputs as source of truth:
   - `docs/specs/<feature>.md`
   - `docs/specs/<feature>.contract.json`
   - `docs/specs/<feature>.traceability.yaml`
2. Map contracts to existing project structure first
3. Extend existing modules before creating new files
4. Generate only minimal compile-ready skeletons
5. Preserve backward-compatible public signatures unless contract declares breaking changes

## Non-Negotiable Constraints

- Never rewrite unrelated files
- Never invent fields not in contract
- Never remove fields without explicit breaking-change declaration
- Never generate mock or fake business data in production path
- Never bypass existing project lint/type rules

## Required Outputs

Produce all artifacts:
- Updated implementation files aligned with contract operations
- `docs/specs/<feature>.codegen.report.json`

`codegen.report.json` must include:
- `feature`
- `state_before`
- `state_after`
- `skill`
- `timestamp`
- `result`
- `blocking_reasons`
- generated_files
- changed_public_signatures
- compatibility_result
- unresolved_contract_items

Report structure must conform to `skills/sdd-orchestrator/sdd-machine-schema.json`.

## Gate Checks

Before declaring success:
- All contract operations map to callable code entry points
- All required input and output fields are represented
- No unresolved contract operation remains
- `compatibility_result` is `pass`
- All checklist items for `spec-to-codebase` pass in `skills/sdd-orchestrator/sdd-gate-checklist.json`

## Failure Handling

When any gate fails:
- Keep state at `SpecValidated`
- Record failures in `codegen.report.json`
- Return control to spec refinement, not manual patching

## Handoff Contract

When successful:
- Emit target state `CodeGenerated`
- Provide changed file list
- Provide codegen report path

The next required skills are:
1. `spec-contract-diff`
2. `spec-driven-test`
