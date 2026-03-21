# Skills Decision Tree

> **Quick Reference** - Find the right skill in 30 seconds

## Start Here

```
About to generate a plan, commit, or make a major decision?
├─ ✅ Run constitution-check FIRST
└─ Then proceed with your task

What is your task?
│
├─ 🤔 Clarifying vague requirements
│   └─→ requirements
│
├─ 🏗️ Making tech decisions / system design
│   └─→ architecture
│
├─ 🎨 Creating UI / design system
│   └─→ design-review
│
├─ 🐛 Fixing a bug / debugging
│   └─→ debugging
│
├─ 🧪 Writing tests / TDD / quality
│   └─→ qa
│
├─ 📋 Implementing a feature (cross-module)
│   └─→ sdd-orchestrator
│
└─ 🚀 Simple change (single file, clear scope)
    └─→ Just do it!
```

> ⚠️ **constitution-check is MANDATORY** before: plans, reviews, commits, phase advancement

---

## Decision Tree Detail

### 1. Requirements Unclear?

```
User: "I want to build something..."
├─ Ask questions first
└─→ requirements
```

**requirements handles:**
- Vague user intent
- Multiple possible interpretations
- User story creation
- Acceptance criteria definition

---

### 2. Need Tech Decisions?

```
About to implement but don't know tech stack?
├─ Need to select technologies
└─→ architecture
```

**architecture handles:**
- Tech stack selection
- System component design
- Data model design
- API design
- Recording tech decisions

---

### 3. Building UI?

```
Building frontend or need design guidelines?
├─ No design system exists
└─→ design-review
```

**design-review handles:**
- Design system creation
- AI slop detection
- UI review
- Design tokens

---

### 4. Bug or Test Failure?

```
Something is broken or unexpected behavior?
├─ Root cause unclear → debugging
├─ Test failing → qa
└─ Known fix → Just fix it
```

**debugging handles:**
- Root cause analysis
- SURVEY → PATTERN → HYPOTHESIS → IMPLEMENT
- Bug fixes
- Stop after 3 failed attempts

**qa handles:**
- Test-driven development
- Red-green-refactor
- Test coverage
- E2E testing

---

### 5. Multi-Module Feature?

```
Feature involves:
├─ Multiple modules
├─ API contracts
└─ Cross-module boundaries?
    └─→ sdd-orchestrator
```

**sdd-orchestrator handles:**
- SDD state machine
- Gate enforcement
- Spec-driven development
- Contract management

---

## SDD Sub-Decision Tree

When in SDD mode:

```
Current State?
│
├─ Ideation/Explore
│   └─→ spec-architect (create spec + contracts)
│
├─ SpecCheckpoint
│   └─→ spec-to-codebase (implement from spec)
│
├─ Build
│   ├─ Code vs spec drift? → spec-contract-diff
│   └─ Run tests? → qa (spec-driven-test)
│
├─ Verify
│   └─→ spec-traceability (verify coverage)
│
└─ ReleaseReady
    └─→ sdd-release-guard (final gate)
```

---

## Quick Reference Card

| Situation | Skill | Key Question |
|-----------|-------|--------------|
| "About to plan/commit?" | `constitution-check` | Rules satisfied? |
| "What do they want?" | `requirements` | Requirements clear? |
| "What tech to use?" | `architecture` | Tech stack decided? |
| "Building UI?" | `design-review` | Design system exists? |
| "Something broke" | `debugging` | Root cause known? |
| "Write tests" | `qa` | TDD or spec-driven? |
| "Cross-module feature" | `sdd-orchestrator` | API contracts defined? |

---

## Skill Categories

```
┌─────────────────────────────────────────────────────────────┐
│                      Self-Awareness                          │
│                    context-tracker                           │
│         (Use at BEGIN, after actions, at END)                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      Compliance                             │
│                    constitution-check                        │
│         (MANDATORY before plans, reviews, commits)          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Vibe Skills (Discovery)                   │
│  requirements │ architecture │ design-review │ debugging    │
│       ↓              ↓              ↓             ↓          │
│    Clarify        Tech           UI            Fix          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    QA Skills (Quality)                       │
│                         qa                                   │
│           (TDD + Spec-driven + E2E testing)                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    SDD Skills (Formal)                       │
│  sdd-orchestrator → spec-architect → spec-contract-diff     │
│                            ↓                                 │
│                     spec-traceability                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

| Mistake | Correct Choice |
|---------|---------------|
| Using SDD for single file | Just implement directly |
| Skipping requirements | `requirements` first |
| Debugging without method | `debugging` skill |
| Not using context-tracker | Use at every checkpoint |
| SDD for internal logic only | Use TDD in `qa` instead |

---

## File Location

This decision tree is available at:
- `skills/SKILL_DECISION.md`
- Referenced in `AGENTS.md`
- Linked from each skill's "Quick Decision" section
