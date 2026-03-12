---
name: "sdd-release-guard"
description: "Applies final SDD release gates and rollback readiness checks. Invoke only after ContractVerified state."
---

# SDD Release Guard

Applies final release governance and decides whether a feature can move from `ContractVerified` to `Released`.

## Mandatory Entry Conditions

All must be true:
- Current state is `ContractVerified`
- Contract diff report result is `pass`
- Test report result is `pass`
- Traceability completeness is 100%

## Invocation Alignment

- If `sdd-orchestrator` is present, it is the only state-transition entry
- Direct invocation is limited to read-only release-readiness analysis
- Direct invocation must not promote state; control returns to `sdd-orchestrator`

Generate:
- `.sdd-spec/specs/<feature>.release.guard.json`

Generate:
- `docs/specs/<feature>.release.guard.json`

Required fields:
- `feature`
- `state_before`
- `state_after`
- `skill`
- `timestamp`
- `result`
- `blocking_reasons`
- `gate_results`
- `feature_flag_plan`
- `observability_checks`
- `rollback_plan`
- `release_decision`

Report structure must conform to `skills/sdd-orchestrator/sdd-machine-schema.json`.

## Gate Set

Release decision is `pass` only if all checks pass:
- Compatibility check
- Contract test gate
- Acceptance test gate
- Traceability gate
- Feature flag availability
- Rollback command and threshold completeness
- All checklist items for `sdd-release-guard` pass in `skills/sdd-orchestrator/sdd-gate-checklist.json`

## Failure Policy

If any gate fails:
- Set `release_decision` to `fail`
- Keep state at `ContractVerified`
- Record blocked gates with explicit reason

## Success Policy

If all gates pass:
- Set `release_decision` to `pass`
- Promote state to `Released`
- Record release timestamp and guard version
