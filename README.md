# SDD-Spec Skills

[中文说明](./README.zh-CN.md)

SDD-Spec Skills is an open-source **strict Spec-Driven Development (SDD) skills bundle**.
It combines state-machine orchestration and gate validation to turn feature delivery into a trackable, verifiable, and releasable workflow.

## LAP Version Tags

- `lap-v1-strict-sdd`: baseline strict SDD workflow with mandatory heavy gates for most tasks
- `lap-v2-adaptive-sdd`: adaptive workflow with risk-based gates and lighter exploration path

## LAP v2 Differential Design

LAP v2 keeps traceability and release safety from v1, but removes excessive ceremony that blocks high-speed iteration.

- Context granularity upgrade: replace 2-5 minute atomic slicing with bounded vertical slices that preserve architecture context
- Spec sync upgrade: move from manual always-on sync to checkpoint-based sync (`SpecCheckpoint`) with generated delta summary
- Worktree policy upgrade: use risk-tier trigger, only mandatory for high-risk multi-module or parallel work
- Gate policy upgrade: split into `Explore`, `Build`, and `Release` modes, each with different mandatory checks

### v2 State Flow

`Ideation -> Explore -> SpecCheckpoint -> Build -> Verify -> ReleaseReady -> Released`

### v2 State-Skill Mapping

| State | Primary Skills | Purpose |
|-------|----------------|--------|
| `Ideation` | `spec-architect` | Convert fuzzy requirements to executable specs |
| `Explore` | `spec-architect`, `spec-traceability` | Architecture exploration, optional spec snapshot |
| `SpecCheckpoint` | `spec-architect` | Spec validation and sync with delta summary |
| `Build` | `spec-to-codebase`, `spec-contract-diff`, `spec-traceability` | Code generation and focused validation |
| `Verify` | `spec-driven-test`, `spec-traceability` | Contract verification and test coverage |
| `ReleaseReady` | `sdd-release-guard` | Final release gates and rollback readiness |
| `Released` | - | Feature delivered |

`Ideation -> Explore -> SpecCheckpoint -> Build -> Verify -> ReleaseReady -> Released`

### v2 Mode Matrix

- Explore mode: local experiments, architecture notes, optional spec snapshot
- Build mode: implementation and focused validation, checkpoint spec sync required
- Release mode: full contract checks, traceability pass, release guard pass

### Fast Path Mode

For simple requirements (config changes, documentation, bug fixes), SDD-Spec Skills supports a **fast path** mode that skips non-essential gates:

```bash
# Use fast path config template
python skills/sdd-orchestrator/validate-sdd.py --config skills/sdd-orchestrator/validate-sdd.config.fast-path.json

# Or via CLI
python skills/sdd-orchestrator/validate-sdd.py --fast-path true --fast-path-skips spec-traceability spec-contract-diff
```

**Fast Path Characteristics:**

| Feature | Standard Mode | Fast Path |
|---------|--------------|-----------|
| Required skills | 6 skills | 4 skills (min) |
| Traceability | Mandatory | Optional |
| Contract diff | Required | Optional |
| Gate checks | Full | Minimal |

## Why This Toolkit

MJ|- Unified state flow: `Ideation -> Explore -> SpecCheckpoint -> Build -> Verify -> ReleaseReady -> Released`
- Unified artifact constraints: spec, contract, tests, traceability matrix, release guard report
- Unified machine validation: `validate-sdd.py` checks skill consistency and gate completeness
- Multi-tool compatibility: supports both flat and multi-layer `skills` layouts

## Included Skills

- `sdd-orchestrator`: state-machine entry and routing
- `spec-architect`: spec and contract design
- `spec-to-codebase`: implementation generation from spec
- `spec-contract-diff`: contract drift detection
- `spec-driven-test`: spec-based testing gate
- `spec-traceability`: requirement-contract-code-test traceability
- `sdd-release-guard`: final pre-release gate

## Artifact Storage

All SDD artifacts are stored in the `.sdd-spec` directory to keep them separate from project code:

```text
.sdd-spec/
  specs/              # Spec, contract, traceability files
    <feature>.md
    <feature>.contract.json
    <feature>.traceability.yaml
    <feature>.state.json
    ...
  tests/specs/       # Test files
    <feature>.contract.spec.*
    <feature>.acceptance.spec.*
    ...
```

> **Note**: The `.sdd-spec` directory is automatically ignored by version control (via `.gitignore`).

## Directory Layout

```text
skills/
  sdd-orchestrator/
    sdd-machine-schema.json
    sdd-gate-checklist.json
    validate-sdd.py
    validate-sdd.config.single-layer.json
    validate-sdd.config.multi-layer.json
  spec-architect/
  spec-to-codebase/
  spec-contract-diff/
  spec-driven-test/
  spec-traceability/
  sdd-release-guard/
```

## Quick Start

1) Run default validation (scans `<root>/skills`):

```bash
python skills/sdd-orchestrator/validate-sdd.py
```

2) Use the single-layer template:

```bash
python skills/sdd-orchestrator/validate-sdd.py --config skills/sdd-orchestrator/validate-sdd.config.single-layer.json
```

3) Use the multi-layer template:

```bash
python skills/sdd-orchestrator/validate-sdd.py --config skills/sdd-orchestrator/validate-sdd.config.multi-layer.json
```

4) Initialize a new project with bootstrap tool:

```bash
# Create new project structure
python skills/sdd-orchestrator/bootstrap-sdd.py init ./my-project

# Add a new feature
python skills/sdd-orchestrator/bootstrap-sdd.py add my-feature ./my-project

# Add skills directory
python skills/sdd-orchestrator/bootstrap-sdd.py add-skills ./my-project
```


## Example Output

A successful validation run looks like this:

```text
SDD validation passed
Root: D:\Code\aaa
Skills paths:
- D:\Code\aaa\skills
Schema: D:\Code\aaa\skills\sdd-orchestrator\sdd-machine-schema.json
Checklist: D:\Code\aaa\skills\sdd-orchestrator\sdd-gate-checklist.json
```

If `SDD validation passed` is shown, skill coverage, state enums, and gate checklist structure are all consistent.

## Configuration

`validate-sdd.py` supports three configuration sources: CLI args, environment variables, and JSON config files.

Precedence:

- `root_path`: CLI > environment > config file > script default
- `skills_paths`: CLI + environment + config file (merged and deduplicated)

Common CLI options:

- `--root-path`
- `--skills-path` (repeatable)
- `--orchestrator-path`
- `--schema-path`
- `--checklist-path`
- `--recursive-search true|false`
- `--config <json>`

Supported environment variables:

- `SDD_VALIDATE_CONFIG`
- `SDD_ROOT_PATH`
- `SDD_SKILLS_PATHS`
- `SDD_ORCHESTRATOR_PATH`
- `SDD_SCHEMA_PATH`
- `SDD_CHECKLIST_PATH`
- `SDD_RECURSIVE_SEARCH`

## Common Failures and Fixes

- `Unable to resolve sdd-orchestrator path from configured skills paths`
  - Ensure `skills_paths` points to real skill roots
  - Ensure `sdd-orchestrator` contains both `sdd-machine-schema.json` and `sdd-gate-checklist.json`
- `SKILL.md not found for <skill>`
  - Ensure the target skill directory exists
  - For nested layouts, enable `--recursive-search true`
- `missing schema reference` or `missing checklist reference`
  - Ensure each skill `SKILL.md` references both schema and checklist
- `State enum mismatch between schema and checklist`
  - Align state enums between `sdd-machine-schema.json` and `sdd-gate-checklist.json`
- `Checklist section incomplete for <skill>`
  - Ensure checklist includes `entry_state`, `required_outputs`, and `gate_checks`

## Open Source Release Notes

- Keep all skill directories under top-level `skills/`
- Avoid tool-private nesting like `.trae/skills/`
- Run validation before every release
- Commit `LICENSE` and `.gitignore` together with functional changes

## License

This project is licensed under MIT. See [LICENSE](./LICENSE).
