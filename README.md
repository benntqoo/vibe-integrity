# Vibe Integrity

[中文说明](./README.zh-CN.md)

Vibe Integrity is an **AI Project Memory & Safety System** designed for AI-assisted development. It prevents false completion claims and provides structured project knowledge for rapid AI understanding.

## Overview

Vibe Integrity solves two critical problems in AI-assisted development:

1. **Completion Guard** - Detects when AI falsely claims work is complete
2. **Architecture Memory** - Structured project knowledge for AI quick understanding

## Quick Start

```bash
# Initialize project
vic init --name "My Project" --tech "Node.js,Vue,PostgreSQL"

# Record a technical decision
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database" --reason "Need ACID"

# Validate
vic validate

# Check status
vic status
```

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `vic init` | - | Initialize .vibe-integrity/ |
| `vic rt` | `record-tech` | Record technical decision |
| `vic rr` | `record-risk` | Record risk |
| `vic rd` | `record-dep` | Record dependency |
| `vic check` | - | Check code alignment |
| `vic validate` | - | Full validation |
| `vic status` | - | Show project status |
| `vic search` | - | Search records |
| `vic history` | - | Show event history |
| `vic export` | - | Export data |
| `vic import` | - | Import data |

See [cmd/vic/README.md](./cmd/vic/README.md) for full documentation.

## Directory Structure

```
project/
├── cmd/
│   └── vic/                    # CLI tool
│       ├── vic                 # Main CLI
│       ├── README.md           # English docs
│       ├── README_cn.md        # Chinese docs
│       └── *.py                # Scripts
│
├── skills-base/                # Skills definitions
│   ├── vibe-integrity/SKILL.md
│   ├── vibe-think/SKILL.md
│   └── vibe-debug/SKILL.md
│
├── docs/                       # Design docs
│   └── *.md
│
├── .vibe-integrity/           # Project memory
│   ├── project.yaml
│   ├── tech-records.yaml
│   ├── risk-zones.yaml
│   ├── dependency-graph.yaml
│   ├── events.yaml
│   └── state.yaml
│
├── .pre-commit-config.yaml
└── requirements.txt
```

## Core Files

| File | Purpose |
|------|---------|
| `project.yaml` | Project metadata, tech stack |
| `tech-records.yaml` | Technical decisions |
| `risk-zones.yaml` | High-risk areas |
| `dependency-graph.yaml` | Module dependencies |
| `events.yaml` | Event history (append-only) |
| `state.yaml` | Current state (generated) |

## AI Quick Start

When AI starts on this project, read in order:

```
1. .vibe-integrity/project.yaml    → Project status, tech stack
2. .vibe-integrity/risk-zones.yaml → High-risk areas
3. .vibe-integrity/tech-records.yaml → Why system is designed this way
```

**Result**: AI understands project in ~15 seconds.

## Workflow

| Scenario | Command |
|----------|---------|
| Start new project | `vic init` |
| Made a decision | `vic rt` |
| Found a risk | `vic rr` |
| AI claims "done" | `vic check` |
| Before commit | `vic validate` |
| Backup memory | `vic export` |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `vibe-integrity` | Core CLI and validation |
| `vibe-think` | Requirement clarification |
| `vibe-debug` | Systematic debugging |

## Installation

```bash
# Dependencies
pip install pyyaml filelock pre-commit

# Linux/macOS
chmod +x cmd/vic/vic
sudo ln -s $(pwd)/cmd/vic/vic /usr/local/bin/vic

# Windows PowerShell
Set-Alias vic "python D:\path\to\cmd\vic\vic"

# Install pre-commit hooks
pre-commit install
```

## License

MIT License. See [LICENSE](./LICENSE).
