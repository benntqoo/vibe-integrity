# Context Tracker Examples

## Example 1: Task BEGIN

**Scenario**: Starting a new feature implementation

```yaml
# .vic-sdd/context.yaml (before)
context:
  known: []
  inferred: []
  assumed: []
  unknown: []
signals:
  positive: []
  warnings: []
  blockers: []
confidence: 0.0

# Steps:
# 1. Read current context (empty)
# 2. Update knowledge map with project info
# 3. Record signals (new task started)
# 4. Calculate confidence
# 5. Write context.yaml

# .vic-sdd/context.yaml (after)
context:
  known:
    - Project uses React + TypeScript
    - Main entry point is src/index.ts
    - SPEC exists at docs/SPEC.md
  inferred:
    - Need to understand current codebase structure
  assumed: []
  unknown:
    - User requirements details
    - Specific implementation approach
signals:
  positive: ["task_begin"]
  warnings: []
  blockers: []
confidence: 0.8
```

## Example 2: After Implementation

**Scenario**: Completed a major refactoring

```yaml
# .vic-sdd/context.yaml (before)
context:
  known: [...]
  inferred: [...]
  assumed: [...]
  unknown: [...]
signals:
  positive: [...]
  warnings: ["assumed_api_compatibility"]
  blockers: [...]
confidence: 0.6

# Steps:
# 1. Read current context
# 2. Update knowledge with refactoring results
# 3. Record signals (refactoring_done, api_changes)
# 4. Check for new blockers
# 5. Recalculate confidence

# .vic-sdd/context.yaml (after)
context:
  known:
    - Refactored auth module
    - API endpoints changed
    - Backwards compatibility maintained
  inferred: []
  assumed: []
  unknown: []
signals:
  positive: ["task_begin", "refactoring_done"]
  warnings: ["assumed_api_compatibility"]
  blockers: []
confidence: 0.9
```

## Example 3: Confidence Drop

**Scenario**: Encountered unexpected issues

```yaml
# .vic-sdd/context.yaml (before)
context:
  known: [...]
  inferred: [...]
  assumed: [...]
  unknown: [...]
signals:
  positive: [...]
  warnings: [...]
  blockers: []
confidence: 0.8

# Steps:
# 1. Read current context
# 2. Discover unknown issues
# 3. Record blockers
# 4. Confidence drops below threshold
# 5. Request human help

# .vic-sdd/context.yaml (after)
context:
  known: [...]
  inferred: [...]
  assumed: [...]
  unknown: [...]
signals:
  positive: [...]
  warnings: [...]
  blockers: ["unknown_dependency_issue", "external_api_failure"]
confidence: 0.3
```

## Example 4: Decision Documentation

**Scenario**: Making important technical decisions

```yaml
# .vic-sdd/context.yaml (before)
context:
  known: [...]
  inferred: [...]
  assumed: [...]
  unknown: [...]
signals:
  positive: [...]
  warnings: [...]
  blockers: [...]
confidence: 0.7

# Steps:
# 1. Read current context
# 2. Document decision alternatives
# 3. Record decision made
# 4. Update knowledge map
# 5. Recalculate confidence

# .vic-sdd/context.yaml (after)
context:
  known:
    - Chose PostgreSQL over MySQL
    - Decision based on performance requirements
    - Documented in tech-decisions.md
  inferred: []
  assumed: []
  unknown: [...]
signals:
  positive: [...]
  warnings: [...]
  blockers: []
confidence: 0.8
```