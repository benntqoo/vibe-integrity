# Skills Base - Path Configuration

## Directory Structure

```
D:\Code\aaa\
├── skills-base/           # Core capabilities (Completion Guard + Architecture Memory)
│   ├── skill-registry.json    # Skill registry (auto-generated)
│   ├── vibe-guard/
│   │   ├── SKILL.md
│   │   ├── validate-vibe-guard.py
│   │   └── vibe-guard.config.json    # NEW
│   ├── vibe-design/
│   │   ├── SKILL.md
│   │   └── vibe-design.py           # NEW - to be implemented
│   ├── vibe-integrity-debug/
│   │   ├── SKILL.md
│   │   └── vibe_integrity_debug.py  # NEW - to be implemented
│   ├── vibe-integrity-writer/
│   │   ├── SKILL.md
│   │   └── vibe-integrity-writer.py
│   ├── vibe-integrity/
│   │   ├── SKILL.md
│   │   ├── validate-vibe-integrity.py
│   │   └── template/               # NEW
│   │       ├── project.schema.json
│   │       ├── tech-records.schema.json
│   │       └── ...
│   └── cli.py                      # NEW - unified CLI
│
├── skills-sdd/            # SDD Workflow (State Machine + Gates)
│   ├── sdd-orchestrator/
│   ├── spec-architect/
│   ├── spec-to-codebase/
│   ├── spec-contract-diff/
│   ├── spec-driven-test/
│   ├── sdd-release-guard/
│   └── spec-traceability/
│
├── .vibe-integrity/       # Project architecture memory
│   ├── project.yaml
│   ├── tech-records.yaml
│   ├── dependency-graph.yaml
│   ├── module-map.yaml
│   ├── risk-zones.yaml
│   ├── schema-evolution.yaml
│   └── ...
│
└── .sdd-spec/            # SDD state and artifacts
    ├── specs/
    │   └── <feature>.state.json
    └── vibe-guard-report.json
```

## Path Aliases

| Alias | Full Path | Usage |
|-------|-----------|-------|
| `skills-base` | `D:/Code/aaa/skills-base` | Core skills |
| `skills-sdd` | `D:/Code/aaa/skills-sdd` | SDD workflow |
| `.vibe-integrity` | `<project>/.vibe-integrity` | Architecture memory |
| `.sdd-spec` | `<project>/.sdd-spec` | SDD state |

## Usage in Skills

### From skills-base:

```python
# Always use absolute paths or aliases
SKILLS_BASE = Path("D:/Code/aaa/skills-base")
VIBE_DIR = Path(".vibe-integrity")
SDD_SPEC_DIR = Path(".sdd-spec")
```

### From skills-sdd:

```python
SKILLS_SDD = Path("D:/Code/aaa/skills-sdd")
VIBE_DIR = Path(".vibe-integrity")
SDD_SPEC_DIR = Path(".sdd-spec")
```

## Migration Notes

### Old → New Path Mappings

| Old Path | New Path | Status |
|----------|----------|--------|
| `skills/vibe-guard/` | `skills-base/vibe-guard/` | ✅ Renamed |
| `skills/vibe-integrity/` | `skills-base/vibe-integrity/` | ✅ Renamed |
| `.sdd-spec/vibe-guard.config.json` | `skills-base/vibe-guard/vibe-guard.config.json` | ✅ Created |
| `skills/sdd-orchestrator/` | `skills-sdd/sdd-orchestrator/` | ✅ Renamed |

### Breaking Changes

1. All skills must reference `skills-base/` or `skills-sdd/` explicitly
2. Config files now co-located with their skill implementation
3. YAML templates moved to `skills-base/vibe-integrity/template/`

## Validation

Run to validate path consistency:

```bash
python skills-base/skill-registry.json --validate-paths
```
