---
name: "sdd-orchestrator"
description: "Coordinates strict SDD state transitions and gate checks. Invoke as the only entry point for feature delivery."
---

# SDD Orchestrator

This skill is the single controller for strict SDD execution.

## Mission

Enforce one-way, auditable, and recoverable feature progression:
`Ideation -> SpecDraft -> SpecValidated -> CodeGenerated -> Implemented -> ContractVerified -> Released`

## Invocation Policy

- Always invoke this skill first for any feature change
- Other SDD skills must run only when directed by this skill
- Direct invocation of downstream skills without matching state is invalid

## Canonical Enums

- `state`: `Ideation` | `SpecDraft` | `SpecValidated` | `CodeGenerated` | `Implemented` | `ContractVerified` | `Released`
- `result`: `pass` | `fail` | `blocked`
- `compatibility_mode`: `backward` | `forward` | `strict`

## Machine Contracts

- Schema file: `skills/sdd-orchestrator/sdd-machine-schema.json`
- Gate checklist: `skills/sdd-orchestrator/sdd-gate-checklist.json`
- Validation command: `python skills/sdd-orchestrator/validate-sdd.py`
- Configurable command: `python skills/sdd-orchestrator/validate-sdd.py --skills-path <skills_path1> --skills-path <skills_path2> --recursive-search true --config <config.json>`
- Single-layer template: `skills/sdd-orchestrator/validate-sdd.config.single-layer.json`
- Multi-layer template: `skills/sdd-orchestrator/validate-sdd.config.multi-layer.json`
- All SDD skills must follow these machine-readable definitions

## Required Inputs

- Feature identifier
- Current state record
- Existing spec artifacts for that feature, if any

Track feature state in:
- `.sdd-spec/specs/<feature>.state.json`

Track feature state in:
- `docs/specs/<feature>.state.json`

Minimum schema:
- `feature`
- `current_state`
- `last_gate`
- `last_skill`
- `updated_at`
- `result`
- `blocked_reason`
- `artifacts`

## Routing Rules

> **Note**: `spec-traceability` is a **verification-only skill** - it does NOT change state. It validates completeness and blocks progression if gates fail.

- If state is `Ideation` or `SpecDraft`, call `spec-architect`
- After spec creation or update, call `spec-traceability` (verification only, no state change)
- If state is `SpecValidated`, call `spec-to-codebase`
- After code generation, call `spec-traceability` (verification only, no state change)
- If state is `CodeGenerated` or `Implemented`, call `spec-contract-diff`
- If diff passes, call `spec-driven-test`
- After test generation or update, call `spec-traceability` (verification only, no state change)
- If tests pass and state becomes `ContractVerified`, call `sdd-release-guard`

- If state is `Ideation` or `SpecDraft`, call `spec-architect`
- After spec creation or update, call `spec-traceability`
- If state is `SpecValidated`, call `spec-to-codebase`
- After code generation, call `spec-traceability`
- If state is `CodeGenerated` or `Implemented`, call `spec-contract-diff`
- If diff passes, call `spec-driven-test`
- After test generation or update, call `spec-traceability`
- If tests pass and state becomes `ContractVerified`, call `sdd-release-guard`

## Gate Governance

- Never skip failed gates
- Never downgrade compatibility claims silently
- Never promote state without output artifacts
- Always persist block reasons in the state record

## Recovery Rules

- If a skill fails, remain in current valid state
- If contracts change, force return to `SpecDraft`
- If tests fail, set state to `Implemented` with failed IDs

## Completion Rule

Delivery is complete only when:
- State is `Released`
- Release guard report exists
- Traceability matrix is complete
