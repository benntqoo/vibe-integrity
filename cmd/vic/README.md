# vic - Vibe Integrity CLI

Unified CLI for AI project memory and validation.

## Installation

```bash
# Dependencies
pip install pyyaml filelock

# Linux/macOS - Add to PATH
chmod +x vic
sudo ln -s $(pwd)/vic /usr/local/bin/vic

# Windows PowerShell
Set-Alias vic "python D:\path\to\cmd\vic\vic"
```

## Quick Start

```bash
# Initialize project
vic init --name "My Project" --tech "Node.js,Vue,PostgreSQL"

# Record a technical decision
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database" --reason "Need ACID"

# Check status
vic status

# Validate
vic validate
```

---

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `record-tech` | `rt` | Record a technical decision |
| `record-risk` | `rr` | Record a risk |
| `record-dep` | `rd` | Record a dependency |
| `check` | - | Check code alignment |
| `validate` | - | Full validation (check + fold) |
| `fold` | - | Fold events to state |
| `status` | - | Show project status |
| `init` | - | Initialize .vibe-integrity/ |
| `search` | - | Search records |
| `history` | - | Show event history |
| `export` | - | Export data |
| `import` | - | Import data |

---

## Command Reference

### vic init

Initialize `.vibe-integrity/` directory for a project.

```bash
vic init --name <name> --tech <tech-stack>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `--name` | No | Project name |
| `--tech` | No | Tech stack, comma-separated |

**Example:**
```bash
vic init --name "my-saas" --tech "Node.js,Vue,PostgreSQL,Redis"
```

---

### vic record-tech (rt)

Record a technical decision.

```bash
vic rt --id <ID> --title <title> --decision <decision> [options]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `--id` | Yes | Decision ID, e.g. `DB-001`, `AUTH-002` |
| `--title` | Yes | Decision title |
| `--decision` | Yes | The decision |
| `--category` | No | Category: database, auth, frontend, backend, etc. |
| `--reason` | No | Why this decision was made |
| `--impact` | No | Impact level: low, medium, high |
| `--status` | No | Status: planned, in_progress, completed, deprecated |
| `--files` | No | Related files, comma-separated |

**Example:**
```bash
# Basic
vic rt --id DB-001 --title "Use PostgreSQL" --decision "Primary database"

# Full
vic rt --id AUTH-001 \
  --title "JWT Authentication" \
  --decision "Use JWT with refresh tokens" \
  --category auth \
  --reason "Stateless, scalable" \
  --impact high \
  --status in_progress \
  --files "src/auth/,src/middleware/auth.ts"
```

---

### vic record-risk (rr)

Record a risk area.

```bash
vic rr --id <ID> --area <area> --desc <description> [options]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `--id` | Yes | Risk ID, e.g. `RISK-001` |
| `--area` | Yes | Risk area |
| `--desc` | Yes | Risk description |
| `--category` | No | Category |
| `--impact` | No | Impact level: low, medium, high, critical |
| `--status` | No | Status: identified, mitigating, resolved, accepted |

**Example:**
```bash
vic rr --id RISK-001 \
  --area auth-service \
  --desc "JWT token not properly validated" \
  --impact critical \
  --status identified
```

---

### vic record-dep (rd)

Record module dependencies.

```bash
vic rd --module <module> --deps <dependencies>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `--module` | Yes | Module name |
| `--deps` | Yes | Dependencies, comma-separated |

**Example:**
```bash
vic rd --module auth-service --deps user-service,jwt-service,cache-service
```

---

### vic check

Check if code aligns with technical decisions.

```bash
vic check
```

Detects inconsistencies between project code and decisions recorded in `.vibe-integrity/tech-records.yaml`.

**Example output:**
```
✅ All decisions align with code
   total: 9
   pass: 5
   fail: 0
   skip: 1
   unknown: 3
```

---

### vic validate

Run full validation (code alignment + event folding).

```bash
vic validate
```

**Steps:**
1. Code alignment check
2. Fold events to state

**Example output:**
```
🔍 Step 1: Code Alignment Check
----------------------------------------
✅ Code alignment OK

📦 Step 2: Fold Events
----------------------------------------

========================================
✅ All validations passed!
```

---

### vic fold

Fold event history into current state snapshot.

```bash
vic fold
```

Processes events from `events.yaml` and updates `state.yaml`.

---

### vic status

Show current project status.

```bash
vic status
```

**Example output:**
```
📊 Project Status
========================================
Last folded: 2026-03-17
Active decisions: 1
Active risks: 1

Tech records: 10
Risks recorded: 0

📋 Recent Tech Records:
   [FE-002] Use Pinia for state management
   [DB-001] Use PostgreSQL
```

---

### vic search

Search tech records and risk records.

```bash
vic search <query>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `query` | Yes | Search keyword |

**Example:**
```bash
vic search postgres
vic search authentication
```

---

### vic history

View event history.

```bash
vic history [--type <type>] [--limit <count>]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `--type` | No | Filter by event type |
| `--limit` | No | Number to show, default 10 |

**Example:**
```bash
# Show last 5 events
vic history --limit 5

# Show only decision events
vic history --type decision_made
```

---

### vic export

Export `.vibe-integrity/` data to JSON file.

```bash
vic export [--output <file>] [--type <type>]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `--output`, `-o` | No | Output file, default `vibe-integrity-export.json` |
| `--type` | No | Export type: tech, risks, events |

**Example:**
```bash
# Export all
vic export --output backup.json

# Export only tech records
vic export --type tech -o tech-decisions.json
```

---

### vic import

Import data from JSON file.

```bash
vic import <input-file>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `input` | Yes | Input JSON file |

**Example:**
```bash
vic import backup.json
```

Existing records are skipped (by ID), Events are always appended.

---

## Data Files

```
.vibe-integrity/
├── events.yaml          # All events (append-only)
├── state.yaml           # Current state (generated by fold)
├── tech-records.yaml    # Technical decisions
├── risk-zones.yaml      # Risk areas
├── project.yaml         # Project info
└── dependency-graph.yaml # Dependencies
```

---

## Typical Workflows

### Start new project
```bash
vic init --name "My App" --tech "React,Node,PostgreSQL"
```

### Make a decision
```bash
vic rt --id FE-001 --title "Use React Query" --decision "Data fetching layer" --reason "Caching, dedup"
```

### Identify a risk
```bash
vic rr --id RISK-001 --area payment --desc "No idempotency key" --impact high
```

### AI claims "done"
```bash
vic check
```

### Before commit
```bash
vic validate
```

### Migrate/backup project memory
```bash
vic export -o project-memory.json
# ... in new project ...
vic import project-memory.json
```

---

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Failure/Error |
