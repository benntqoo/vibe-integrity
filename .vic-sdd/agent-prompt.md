# VIBE-SDD Workflow Prompt

## Start of Every Session

```
╔══════════════════════════════════════════════════════════════════════╗
║                      VIBE-SDD Development Workflow                     ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  📋 Quick Flow:                                                       ║
║                                                                       ║
║  1. vic init                        → Initialize project              ║
║  2. vic spec init                   → Create SPEC documents          ║
║  3. vic spec gate 0                 → Verify requirements            ║
║  4. vic spec gate 1                 → Verify architecture            ║
║  5. [Implement features]                                           ║
║  6. vic spec gate 2                 → Verify code alignment         ║
║  7. vic spec gate 3                 → Verify test coverage          ║
║  8. vic spec merge                  → Finalize documentation        ║
║                                                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  🚪 Gate Status (Run 'vic gate check' to see current state)         ║
║                                                                       ║
║  Gate 0: Requirements Completeness  [✅/❌]                            ║
║  Gate 1: Architecture Completeness   [✅/❌]                            ║
║  Gate 2: Code Alignment             [✅/❌]                            ║
║  Gate 3: Test Coverage              [✅/❌]                            ║
║                                                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  📁 Read First:                                                       ║
║                                                                       ║
║  1. .vic-sdd/PROJECT.md          → Project status                    ║
║  2. .vic-sdd/SPEC-REQUIREMENTS.md → Requirements & acceptance criteria ║
║  3. .vic-sdd/SPEC-ARCHITECTURE.md → Architecture & tech stack         ║
║  4. .vic-sdd/risk-zones.yaml     → High-risk areas                   ║
║  5. .vic-sdd/context.yaml         → AI self-awareness                ║
║                                                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  ⚠️  Rules:                                                           ║
║                                                                       ║
║  • NEVER skip Gate checks - use 'vic spec gate N' before claiming    ║
║  • Update context.yaml after every meaningful action                   ║
║  • Record tech decisions: vic rt --id XXX --title "..."               ║
║  • Record risks: vic rr --id RISK-XXX --desc "..."                   ║
║                                                                       ║
╚══════════════════════════════════════════════════════════════════════╝
```

## Phase Descriptions

| Phase | Name | Description | Gate |
|-------|------|-------------|------|
| 0 | 需求凝固 | Freeze requirements | Gate 0 |
| 1 | 架构设计 | Design architecture | Gate 1 |
| 2 | 代码实现 | Implement features | Gate 2 |
| 3 | 验证发布 | Test and release | Gate 3 |

## Skill Reference

| Skill | When to Use |
|-------|-------------|
| `requirements` | Clarify vague requirements |
| `architecture` | Design tech stack |
| `design-review` | Build UI design system |
| `debugging` | Fix bugs systematically |
| `qa` | TDD and test coverage |
| `context-tracker` | Track AI self-awareness |
| `sdd-orchestrator` | Manage SDD workflow |

## Quick Commands

```bash
# Check status
vic status
vic spec status
vic gate check --blocking

# Pass gates
vic spec gate 0
vic spec gate 1
vic spec gate 2
vic spec gate 3

# Advance phase (runs gate checks automatically)
vic phase advance --to 1

# Record decisions
vic rt --id DB-001 --title "PostgreSQL" --decision "Primary DB"
vic rr --id RISK-001 --desc "JWT not validated"
```
