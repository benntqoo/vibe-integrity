---
name: "spec-traceability"
description: "Maintains story-to-contract-to-code-to-test mapping. Invoke after any spec or implementation change."
---

# Spec Traceability

> **⚠️ Verification-Only Skill**: This skill does NOT change state. It validates traceability completeness and blocks progression if gates fail.

Maintains a complete and verifiable linkage across requirements, contracts, implementation, and tests.
name: "spec-traceability"
description: "Maintains story-to-contract-to-code-to-test mapping. Invoke after any spec or implementation change."
---

# Spec Traceability

Maintains a complete and verifiable linkage across requirements, contracts, implementation, and tests.

## Mandatory Entry Conditions

Run when any of these change:
- User stories or acceptance criteria
- Contract operations or schemas
- Public code interfaces
- Contract or acceptance tests

## Invocation Alignment

- If `sdd-orchestrator` is present, it is the only state-transition entry
- Direct invocation is limited to read-only traceability analysis
- Direct invocation must not promote state; control returns to `sdd-orchestrator`

Maintain:
- `.sdd-spec/specs/<feature>.traceability.yaml`
- `.sdd-spec/specs/<feature>.traceability.report.json`

Maintain:
- `docs/specs/<feature>.traceability.yaml`
- `docs/specs/<feature>.traceability.report.json`

Each mapping row must contain:
- `story_id`
- `acceptance_id`
- `contract_operation_id`
- `code_entry_points`
- `test_case_ids`
- `status`

`traceability.report.json` must include:
- `feature`
- `state_before`
- `state_after`
- `skill`
- `timestamp`
- `result`
- `blocking_reasons`
- `completeness`
- `orphan_items`

Report structure must conform to `skills/sdd-orchestrator/sdd-machine-schema.json`.

## Consistency Rules

- No orphan story without acceptance criteria
- No acceptance criterion without contract mapping
- No contract operation without code entry point
- No code entry point without at least one test
- Status may be only `draft`, `implemented`, `verified`

## Gate Rules

The matrix passes only when:
- Mapping completeness is 100%
- No duplicate IDs across rows
- All `verified` rows have passing test case references
- All checklist items for `spec-traceability` pass in `skills/sdd-orchestrator/sdd-gate-checklist.json`

## Failure Policy

On failure:
- Write missing links into matrix
- Block release and contract verification promotion

## Success Policy

On success:
- Publish completeness summary
- Allow `sdd-release-guard` to run when other gates pass
