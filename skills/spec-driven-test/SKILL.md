---
name: "spec-driven-test"
description: "Builds and enforces test gates from spec contracts. Invoke after code generation and before release decisions."
---

# Spec-Driven Test

Converts spec artifacts into mandatory verification suites and blocks promotion when any contract path lacks executable proof.

All conditions must be true:
- Current state is `CodeGenerated` or `Implemented`
- `.sdd-spec/specs/<feature>.contract.json` exists
- `.sdd-spec/specs/<feature>.traceability.yaml` exists
- Contract diff check has passed

All conditions must be true:
- Current state is `CodeGenerated` or `Implemented`
- `docs/specs/<feature>.contract.json` exists
- `docs/specs/<feature>.traceability.yaml` exists
- Contract diff check has passed

If not, run `spec-contract-diff` first.

## Invocation Alignment

- If `sdd-orchestrator` is present, it is the only state-transition entry
- Direct invocation is limited to read-only test planning or gap analysis
- Direct invocation must not promote state; control returns to `sdd-orchestrator`

## State Transition Contract

- Input state: `CodeGenerated` or `Implemented`
- Output state on success: `ContractVerified`
- Output state on failure: `Implemented`

Produce:
- `.sdd-spec/tests/specs/<feature>.contract.spec.*`
- `.sdd-spec/tests/specs/<feature>.acceptance.spec.*`
- `.sdd-spec/specs/<feature>.test.report.json`

Produce:
- `tests/specs/<feature>.contract.spec.*`
- `tests/specs/<feature>.acceptance.spec.*`
- `docs/specs/<feature>.test.report.json`

`test.report.json` must include:
- `feature`
- `state_before`
- `state_after`
- `skill`
- `timestamp`
- `result`
- `blocking_reasons`
- `coverage_summary`
- `failed_ids`

Report structure must conform to `skills/sdd-orchestrator/sdd-machine-schema.json`.

## Test Construction Rules

- One acceptance criterion maps to at least one executable test
- One contract operation maps to at least one success test and one failure test
- Each documented error code maps to at least one assertion
- Tests verify runtime behavior through public interfaces only
- External dependencies may be isolated, but business logic cannot be replaced

## Gate Checks

All must pass:
- Traceability coverage for stories and acceptance criteria is 100%
- Contract operation coverage is 100%
- Error code coverage is 100%
- No flaky test markers remain
- Test report marks overall result as `pass`
- All checklist items for `spec-driven-test` pass in `skills/sdd-orchestrator/sdd-gate-checklist.json`

On any failure:
- Emit `.sdd-spec/specs/<feature>.test.report.json` with failed IDs
- Keep state at `Implemented`
- Block release guard invocation

On any failure:
- Emit `docs/specs/<feature>.test.report.json` with failed IDs
- Keep state at `Implemented`
- Block release guard invocation

## Handoff Contract

When successful:
- Emit target state `ContractVerified`
- Publish test report path
- Publish coverage summary

The next required skill is `sdd-release-guard`.
