# vic-go

VIBE-SDD CLI written in Go.

## Features

- Single binary, no dependencies required
- Fast startup time
- Cross-platform (Linux, macOS, Windows)
- Full support for all vic commands

## Installation

### From Source

```bash
# Clone and build
cd cmd/vic-go
make build

# Install to PATH
sudo ln -s $(pwd)/vic /usr/local/bin/vic

# Or use make install
make install
```

### Pre-built Binaries

Download from [Releases](https://github.com/vic-sdd/vic/releases)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VIC_DIR` | `.vic-sdd` | Override VIC directory name |
| `VIC_PROJECT_DIR` | (current dir) | Override project directory |
| `VIC_OUTPUT` | `plain` | Output format (json/yaml/plain) |
| `VIC_VERBOSE` | `false` | Verbose output |

### Examples

```bash
# Use custom VIC directory
VIC_DIR=.my-vic vic init

# Use custom project directory
VIC_PROJECT_DIR=/path/to/project vic status

# JSON output
VIC_OUTPUT=json vic status
```

## Usage

```bash
# Initialize project
vic init --name "My Project" --tech "Go,PostgreSQL"

# Record technical decision
vic record tech --id DB-001 --title "Use PostgreSQL" --decision "Primary DB"

# Record risk
vic record risk --id RISK-001 --area auth --desc "JWT not validated"

# Check code alignment
vic check

# Full validation
vic validate

# Show status
vic status

# Search records
vic search postgres

# SPEC management
vic spec init
vic spec gate 0
```

## Development

```bash
# Build
make build

# Build for all platforms
make build-all

# Run tests
make test

# Run locally
make run ARGS="--help"
```

## Commands

### Core Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `init` | - | Initialize .vic-sdd/ |
| `status` | - | Show project status |
| `check` | - | Check code alignment |
| `validate` | - | Full validation (check + fold) |
| `fold` | - | Fold events to state |
| `search` | - | Search records |
| `history` | - | Show event history |
| `export` | - | Export data |
| `import` | - | Import data |

### Record Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `record tech` | `rt` | Record technical decision |
| `record risk` | `rr` | Record risk |
| `record dep` | `rd` | Record dependency |

### SPEC Commands

| Command | Description |
|---------|-------------|
| `spec init` | Initialize SPEC documents |
| `spec status` | Show SPEC status |
| `spec gate [0-3\|1.5]` | Run SPEC gate check |
| `spec hash` | Check SPEC file hashes and detect changes |
| `spec diff` | Detect SPEC changes since last check |
| `spec changes` | Show SPEC change history |
| `spec watch` | Monitor SPEC changes and auto-run drift detection |
| `spec merge` | Merge SPEC to final documents |

### Phase & Gate Commands

| Command | Description |
|---------|-------------|
| `phase status` | Show current phase status |
| `phase advance --to N` | Advance to phase N |
| `phase check` | Check phase requirements |
| `gate status` | Show all gate status |
| `gate pass --gate N` | Mark gate N as passed |
| `gate check [--blocking]` | Check gates (for pre-commit) |
| `gate smart [--execute]` | Smart gate selection based on risk |

### Semantic Search

| Command | Description |
|---------|-------------|
| `ask <query>` | Semantic search about codebase |
| `sync` | Sync embedding index for vic ask |
| `assess` | Intelligent change assessment |

### Autonomous Mode

| Command | Description |
|---------|-------------|
| `auto start` | Start autonomous mode |
| `auto status` | Show auto mode status |
| `auto pause` | Pause autonomous mode |
| `auto resume` | Resume autonomous mode |
| `auto stop` | Stop autonomous mode |

### Cost Tracking

| Command | Description |
|---------|-------------|
| `cost init` | Initialize cost tracking |
| `cost status` | Show cost tracking status |
| `cost set-budget <amount>` | Set budget ceiling |
| `cost add --input N --output N --cost N` | Add cost record |

### Product & Planning

| Command | Description |
|---------|-------------|
| `product record` | Record product redesign decision |
| `product list` | List product decisions |
| `product modes` | Show four product modes |
| `replan trigger` | Trigger adaptive replan |
| `replan list` | List replan history |
| `replan show <id>` | Show replan details |

### Quality Assurance

| Command | Description |
|---------|-------------|
| `slop scan` | Scan for AI slop patterns |
| `slop report` | Show last scan report |
| `slop list` | List configured patterns |
| `slop fix` | Auto-fix AI slop patterns |
| `qa init` | Initialize QA setup |
| `qa quick` | Quick smoke test |
| `qa full` | Full application test |
| `qa screenshot --name <name>` | Capture screenshot |
| `qa report` | Show QA report |

### Development Tools

| Command | Description |
|---------|-------------|
| `tdd start --feature <name>` | Start TDD session |
| `tdd red --test <name>` | RED phase - write failing test |
| `tdd green --test <name>` | GREEN phase - make it pass |
| `tdd refactor` | REFACTOR phase |
| `tdd status` | Show TDD status |
| `tdd checkpoint --note <text>` | Save TDD checkpoint |
| `tdd history` | Show TDD history |
| `debug start --problem <desc>` | Start debug session |
| `debug survey` | Gather evidence |
| `debug pattern` | Find similar issues |
| `debug hypothesis --explain <text>` | Form and test hypothesis |
| `debug implement --fix <text>` | Implement fix |
| `debug status` | Show debug status |
| `debug report` | Generate debug report |

### Design & Dependencies

| Command | Description |
|---------|-------------|
| `design init` | Initialize design system |
| `design consultation` | Design consultation mode |
| `design review` | Design review mode |
| `design audit` | Run design audit |
| `deps scan` | Scan and generate dependency graph |
| `deps list` | List all modules |
| `deps search <pattern>` | Search modules by pattern |
| `deps impact <module>` | Show impact of changing a module |
| `deps callers <module>` | Show who calls a module |
| `sync` | Sync embedding index |

### Skill Documentation

| Command | Description |
|---------|-------------|
| `skill list` | List available skills |
| `skill show <name>` | Show skill documentation |
| `skill activate <name>` | Show how to activate a skill |

## Gate Reference

| Gate | Name | Checks |
|------|------|--------|
| Gate 0 | Requirements Completeness | SPEC-REQUIREMENTS.md structure |
| Gate 1 | Architecture Completeness | SPEC-ARCHITECTURE.md structure |
| Gate 1.5 | Design Completeness | DESIGN.md completeness (optional) |
| Gate 2 | Code Alignment | Code vs SPEC alignment |
| Gate 3 | Test Coverage | Test coverage verification |

## Phase Flow

```
Phase 0: Requirements     → Gate 0, Gate 1
Phase 1: Architecture     → Gate 2, Gate 3
Phase 2: Implementation   → Gate 4, Gate 5
Phase 3: Release          → Gate 6, Gate 7
```

## Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: vic-gate-check
        name: VIBE-SDD Gate Check
        entry: vic gate check --blocking
        language: system
```

## License

MIT
