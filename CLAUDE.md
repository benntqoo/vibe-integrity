# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VIBE-SDD is a Spec-Driven Development system combining structured SDD with flexible Vibe Coding. It provides a workflow for AI-assisted development with quality gates and documentation. The main component is a Go CLI tool (`vic`) that manages project state, SPEC documents, and gate checks.

## Build and Test Commands

```bash
# Build the CLI (from cmd/vic-go)
cd cmd/vic-go && make build

# Run tests
cd cmd/vic-go && make test

# Build for all platforms
cd cmd/vic-go && make build-all

# Install to PATH
cd cmd/vic-go && make install

# Run locally with arguments
cd cmd/vic-go && make run ARGS="--help"
```

## Key CLI Commands

```bash
# Initialize project
vic init --name "Project Name" --tech "Go,PostgreSQL"

# SPEC management
vic spec init                    # Initialize SPEC documents
vic spec status                  # Show SPEC status
vic spec hash                    # Check SPEC hashes and detect changes
vic spec diff                    # Show SPEC changes since last check
vic spec gate 0                  # Requirements completeness
vic spec gate 1                  # Architecture completeness
vic spec gate 2                  # Code alignment with SPEC
vic spec gate 3                  # Test coverage

# Phase and gate management
vic phase advance --to 1         # Advance phase (auto-runs gates)
vic gate check --blocking        # Pre-commit gate check

# Record decisions
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary DB"
vic rr --id RISK-001 --area auth --desc "JWT validation missing"

# Status and validation
vic status                       # Project status
vic check                        # Code alignment check
vic validate                     # Full validation
vic search <term>                # Search records
vic history --limit 10           # Recent events

# Semantic search (requires embedding)
vic ask <query>                  # Ask about the codebase
```

## Architecture

```
cmd/vic-go/
├── main.go                    # Entry point
├── internal/
│   ├── commands/              # CLI command implementations
│   │   ├── root.go           # Root command
│   │   ├── init.go           # vic init
│   │   ├── spec.go           # vic spec
│   │   ├── gate0-3.go        # Gate checks
│   │   ├── hash.go           # SPEC change detection
│   │   └── ...
│   ├── config/                # Configuration management (Viper)
│   ├── checker/               # Code alignment checking
│   ├── types/                 # Type definitions
│   ├── utils/                 # File/YAML utilities
│   └── embedding/             # Semantic search with embeddings
│       ├── store.go          # SQLite vector store
│       ├── embedder.go       # Embedding generation
│       └── chunker/          # Code chunking by language
```

## Skills System

This project uses 5 core skills located in `skills/`:

| Skill | When to Use |
|-------|-------------|
| `context-tracker` | Auto-activated every session; tracks AI self-awareness, confidence, blockers |
| `spec-workflow` | Requirements clarification, architecture design, SPEC creation |
| `implementation` | Code implementation, bug fixes, testing, Gate 2/3 checks |
| `unified-workflow` | Feature delivery, phase transitions, pre-commit, traceability |
| `quick` | Simple single-file changes that don't affect SPEC |

Decision flow: Start with `context-tracker`, then choose based on task type.

## SDD State Machine

```
Ideation -> Explore -> SpecCheckpoint -> Build -> Verify -> ReleaseReady -> Released
              |              |             |         |            |
        spec-workflow              implementation        unified-workflow
```

## Gate Checks

| Gate | Purpose | Checks |
|------|---------|--------|
| Gate 0 | Requirements | SPEC-REQUIREMENTS.md completeness |
| Gate 1 | Architecture | SPEC-ARCHITECTURE.md completeness |
| Gate 2 | Code | Code alignment with SPEC |
| Gate 3 | Tests | Test coverage verification |

## Constitution Rules

Defined in `.vic-sdd/constitution.yaml`. Key rules:
- **SPEC-FIRST**: Update SPEC before changing code
- **SPEC-ALIGNED**: Code must match SPEC
- **GATE-BEFORE-COMMIT**: All gates must pass before commit
- **NO-TODO-IN-CODE**: No TODO/FIXME comments
- **NO-CONSOLE-IN-PROD**: No console.log in production code

## Pre-commit Hooks

Pre-commit is configured in `.pre-commit-config.yaml`:
- `vic-gate-check`: Blocks commits until gates pass
- `vic-spec-drift`: Detects code drift from SPEC

```bash
pre-commit install
pre-commit run --all-files
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VIC_DIR` | `.vic-sdd` | VIC directory name |
| `VIC_PROJECT_DIR` | current dir | Project directory |
| `VIC_OUTPUT` | `plain` | Output format (json/yaml/plain) |
| `VIC_VERBOSE` | `false` | Verbose output |

## Key Files for AI Context

When starting a session, read in order:
1. `.vic-sdd/agent-prompt.md` - Workflow overview
2. `.vic-sdd/PROJECT.md` - Project status and milestones
3. `.vic-sdd/SPEC-REQUIREMENTS.md` - Requirements and acceptance criteria
4. `.vic-sdd/SPEC-ARCHITECTURE.md` - Architecture and tech stack

## Important Notes

- AGENTS.md is the primary AI entry point - keep it concise
- Detailed execution steps are in each skill's SKILL.md
- Gate checks must pass before claiming work is complete
- Always run `vic spec hash` to detect SPEC changes before continuing work
