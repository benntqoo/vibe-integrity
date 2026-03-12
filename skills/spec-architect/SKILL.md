---
name: "spec-architect"
description: "Builds executable specs from ambiguous requirements. Invoke at feature start or when contracts are unclear or incomplete."
---

# Spec Architect

Converts fuzzy requirements into executable, auditable, and gate-ready specifications for strict SDD delivery.

## Mandatory Entry Conditions

Run this skill only when at least one is true:
- Requirements are ambiguous or inconsistent
- Data models or API contracts are missing
- Acceptance criteria are incomplete
- Existing implementation changed behavior without clear contract updates

## Invocation Alignment

- If `sdd-orchestrator` is present, it is the only state-transition entry
- Direct invocation is limited to read-only analysis or refinement planning
- Direct invocation must not promote state; control returns to `sdd-orchestrator`

Produce all artifacts in one pass:
- `.sdd-spec/specs/<feature>.md`
- `.sdd-spec/specs/<feature>.contract.json`
- `.sdd-spec/specs/<feature>.traceability.yaml`
- `.sdd-spec/specs/<feature>.risk.yaml`
- `.sdd-spec/specs/<feature>.spec.report.json`

Produce all artifacts in one pass:
- `docs/specs/<feature>.md`
- `docs/specs/<feature>.contract.json`
- `docs/specs/<feature>.traceability.yaml`
- `docs/specs/<feature>.risk.yaml`
- `docs/specs/<feature>.spec.report.json`

If any output is missing, the state remains `SpecDraft` and code generation is blocked.

## State Transition Contract

- Input state: `Ideation` or `SpecDraft`
- Output state on success: `SpecValidated`
- Output state on failure: `SpecDraft`

`.sdd-spec/specs/<feature>.md` must include:

`docs/specs/<feature>.md` must include:
1. Objective and scope boundaries
2. User stories and acceptance criteria with unique IDs
3. Domain data models
4. API or interface contracts
5. Error taxonomy and retry/idempotency policy
6. Business invariants and non-functional constraints
7. Backward compatibility commitments
8. Rollback and feature-flag strategy

`.sdd-spec/specs/<feature>.contract.json` must include:

`docs/specs/<feature>.contract.json` must include:
- Contract version
- Operations with input and output schemas
- Error codes and messages
- Compatibility mode (`backward`, `forward`, `strict`)
- Breaking change indicator

`.sdd-spec/specs/<feature>.spec.report.json` must include:

`docs/specs/<feature>.spec.report.json` must include:
- `feature`
- `state_before`
- `state_after`
- `skill`
- `timestamp`
- `result`
- `blocking_reasons`
- `coverage_summary`

Report structure must conform to `skills/sdd-orchestrator/sdd-machine-schema.json`.

## Gate Checks

All checks must pass before promoting to `SpecValidated`:
- Every user story maps to at least one acceptance criterion
- Every acceptance criterion maps to at least one contract operation
- Every contract operation defines at least one error scenario
- Compatibility commitments are explicit and testable
- No unresolved `TBD` or `TODO`
- All checklist items for `spec-architect` pass in `skills/sdd-orchestrator/sdd-gate-checklist.json`

## Hard Rules

- Never embed implementation code in spec files
- Never leave unnamed acceptance criteria
- Never permit contract fields without types
- Never mark breaking changes as non-breaking

## Handoff Contract

When this skill succeeds, handoff package must include:
- Spec file path
- Contract file path
- Traceability file path
- Declared target state `SpecValidated`

The next allowed skill is `spec-to-codebase`.
