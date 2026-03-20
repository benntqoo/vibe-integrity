# Requirements Skill

## Overview

Combines vibe-think + vibe-redesign for requirements analysis.

**When to use:**
- User has vague requirements
- Need to clarify what to build
- Product discovery phase

## Process

### Step 1: Understand the Problem

Ask one question at a time:
```
What does your product do?
Who are your users?
What problem does it solve?
What feeling should it convey?
```

### Step 2: Explore with Four Modes

| Mode | Icon | When |
|------|------|------|
| EXPANSION | 🚀 | Explore ambitious possibilities |
| SELECTIVE | ⚖️ | Neutral presentation, let user choose |
| HOLD | 🔒 | Stay focused, no expansions |
| REDUCTION | ✂️ | Find minimum viable version |

### Step 3: Define User Stories

```
As a [user type], I can [action] so that [benefit].

Example:
As a developer, I can run `vic gate check` so that I know 
which gates are blocking before committing.
```

### Step 4: Define Acceptance Criteria

```
Given [context], when [action], then [result].

Example:
Given I'm in a project with SPEC files,
when I run `vic spec gate 0`,
then it validates all requirements are complete.
```

## Output

Update `.vic-sdd/context.yaml`:
```yaml
known:
  - "User wants Gate checks to work"
inferred:
  - "CLI project uses Go"
exploration:
  entries:
    - action: decided
      topic: "Gate 0 validates requirements"
      choice: "Pattern-based validation"
```

Update `.vic-sdd/SPEC-REQUIREMENTS.md`:
- Add User Stories section
- Add Key Features with acceptance criteria
- Add Out of Scope section

## Integration

Before: `vibe-think` or `vibe-redesign`  
After: `spec-architect` to freeze requirements into contracts

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `architecture` | Next step: define tech stack |
| `spec-architect` | Freeze requirements into contracts |
