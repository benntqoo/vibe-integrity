# Architecture Skill

## Overview

Combines vibe-architect for technical design.

**When to use:**
- Requirements are clear
- Need to select technology stack
- Designing system architecture

## Process

### Step 1: Technology Evaluation

```
┌─────────────────────────────────────────┐
│       Technology Evaluation Matrix      │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────┐    ┌─────────┐           │
│  │ Tech A │ vs │ Tech B │           │
│  └────┬────┘    └────┬────┘           │
│       │               │                  │
│       ▼               ▼                  │
│  Evaluation Dimensions                    │
│  • Learning curve                       │
│  • Community ecosystem                   │
│  • Documentation quality                 │
│  • Maintenance status                    │
│  • Team familiarity                     │
│  • Performance                          │
│  • Security                             │
│  • Cost                                 │
└─────────────────────────────────────────┘
```

### Step 2: Architecture Design

```
Requirements Analysis
         │
         ▼
┌─────────────────────┐
│   Tech Selection   │ ← SPEC-REQUIREMENTS.md
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   System Design    │ ← Component diagram
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Data Model       │ ← ER diagram
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   API Contract     │ ← REST/GraphQL
└──────────┬──────────┘
           │
           ▼
      SPEC-ARCHITECTURE.md
```

### Step 3: Record Decisions

```bash
vic rt --id ARCH-001 --title "Choose Go CLI" --decision "Use Go + Cobra" --reason "Single binary, fast startup"
vic rr --id ARCH-RISK-001 --area architecture --desc "No testing framework yet" --impact medium
```

## Required Sections

| Section | Content | Importance |
|---------|---------|------------|
| Tech Stack | Each tech with rationale | ⭐⭐⭐ |
| Architecture | Diagram, module划分 | ⭐⭐⭐ |
| Data Model | Entities, relationships | ⭐⭐⭐ |
| API Design | Contracts, error codes | ⭐⭐ |
| Security | Auth, encryption, protections | ⭐⭐⭐ |

## Integration

Before: `requirements` skill  
After: `spec-architect` to freeze into contracts

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `requirements` | Input from user stories |
| `spec-architect` | Freeze architecture into contracts |
| `qa` | Verify implementation against spec |
