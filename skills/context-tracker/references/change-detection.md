# Change Detection

> Automatic detection of change types for intelligent workflow selection

## Overview

Change detection analyzes git diff, file patterns, and content keywords to automatically determine the type of change being made. This enables zero-decision workflow selection.

## Change Types

### 1. typo_fix

**Definition:** Simple text corrections that don't affect logic.

**Indicators:**
```yaml
files_changed: 1
lines_changed: < 10
no_logic_change: true
patterns:
  - "fix typo"
  - "correct spelling"
  - "update comment"
```

**Detection:**
```bash
# Check file count
git diff --name-only | wc -l
# Result: 1

# Check line count
git diff --stat | grep -oE '[0-9]+ insertion'
# Result: < 10

# Check for logic changes (simplified)
git diff --unified=0 | grep -E "^\+.*(\{|}|if|for|while|function|def|class)"
# Result: empty
```

**Risk:** Minimal
**Auto-Skill:** `quick`
**Gates:** None

---

### 2. rename_refactor

**Definition:** Renaming variables, functions, or files without logic changes.

**Indicators:**
```yaml
files_changed: <= 5
change_type: "rename"
no_logic_change: true
patterns:
  - "rename"
  - "refactor name"
  - "move to"
```

**Detection:**
```bash
# Check file count
git diff --name-only | wc -l
# Result: <= 5

# Detect rename patterns (simplified)
git diff --unified=0 | grep -E "^\-.*old.*\+.*new"
# Or use git's rename detection
git diff --find-renames --name-status
# Result: R100 (rename detected)
```

**Risk:** Low
**Auto-Skill:** `quick`
**Gates:** `gate_2` (optional)

---

### 3. bug_fix

**Definition:** Fixing reported bugs or errors.

**Indicators:**
```yaml
keywords:
  - "fix"
  - "bug"
  - "issue"
  - "error"
  - "patch"
test_added: true
scope: "localized"
```

**Detection:**
```bash
# Check commit message or task description
echo "$TASK_DESCRIPTION" | grep -iE "fix|bug|issue|error"

# Check if test file added
git diff --name-only | grep -E "(test|spec)_"

# Check scope
git diff --stat | wc -l
# Result: < 10 files
```

**Risk:** Medium
**Auto-Skill:** `implementation`
**Gates:** `gate_2`, `gate_3`

---

### 4. feature_addition

**Definition:** Adding new functionality or features.

**Indicators:**
```yaml
keywords:
  - "feat"
  - "add"
  - "new"
  - "implement"
  - "create"
new_functions: true
new_files: true
```

**Detection:**
```bash
# Check commit message or task description
echo "$TASK_DESCRIPTION" | grep -iE "feat|add|new|implement|create"

# Check for new function definitions
git diff --unified=0 | grep -E "^\+.*(function|def|class|export|public)"

# Check for new files
git diff --name-status | grep "^A"
```

**Risk:** High
**Auto-Skill:** `implementation`
**Gates:** `gate_0`, `gate_2`, `gate_3`

---

### 5. architecture_change

**Definition:** Major refactoring or architectural changes.

**Indicators:**
```yaml
files_changed: > 10
spec_files_affected: true
keywords:
  - "refactor"
  - "restructure"
  - "migrate"
  - "architecture"
  - "redesign"
breaking_changes: true
```

**Detection:**
```bash
# Check file count
git diff --name-only | wc -l
# Result: > 10

# Check SPEC impact
git diff --name-only | grep -E "SPEC-.*\.md|\.vic-sdd/"
# Result: non-empty

# Check commit message or task description
echo "$TASK_DESCRIPTION" | grep -iE "refactor|restructure|migrate|architecture"

# Check for breaking changes (simplified)
git diff --unified=0 | grep -E "^\-.*(export|public|interface)"
```

**Risk:** Critical
**Auto-Skill:** `spec-workflow` → `implementation`
**Gates:** All (`gate_0`, `gate_1`, `gate_2`, `gate_3`)

---

## Detection Algorithm

### Pseudocode

```
function detect_change_type(task_description, git_diff):
    // 1. Analyze git diff
    files = git_diff.files_changed
    lines = git_diff.lines_changed
    has_logic_change = analyze_logic_changes(git_diff)

    // 2. Check SPEC impact
    spec_affected = check_spec_files(files)

    // 3. Match keywords
    keywords = extract_keywords(task_description)

    // 4. Determine type (priority order)
    if spec_affected or files > 10:
        return "architecture_change"

    if matches(keywords, ["feat", "add", "new", "implement"]):
        return "feature_addition"

    if matches(keywords, ["fix", "bug", "issue", "error"]):
        return "bug_fix"

    if files <= 5 and not has_logic_change:
        if matches(keywords, ["rename"]):
            return "rename_refactor"
        return "typo_fix"

    return "feature_addition" // default
```

### Priority Matrix

| Priority | Check | Result Type |
|----------|-------|-------------|
| 1 | SPEC affected | `architecture_change` |
| 2 | Files > 10 | `architecture_change` |
| 3 | Keywords: feat/add/new | `feature_addition` |
| 4 | Keywords: fix/bug/error | `bug_fix` |
| 5 | No logic change + rename | `rename_refactor` |
| 6 | No logic change + small | `typo_fix` |
| 7 | Default | `feature_addition` |

---

## Edge Cases

### Ambiguous Changes

When multiple types match:

```yaml
# Example: "Fix bug and refactor module"
# Contains both "fix" and "refactor" keywords

resolution:
  1. Check scope first
  2. Use highest risk type
  3. When in doubt, escalate to higher risk
```

### Mixed Changes

When a single commit contains multiple change types:

```yaml
# Example: Fix bug + add new test helper

approach:
  1. Analyze each file separately
  2. Use the highest risk type for overall assessment
  3. Suggest splitting into multiple commits if appropriate
```

---

## Vic Commands

```bash
# Detect change type
vic assess --type

# Output:
# Change Type: bug_fix
# Confidence: 85%
# Files: 3
# Lines: 47
# SPEC Affected: No
```

---

## Summary

| Change Type | Risk | Files | Lines | Logic | SPEC | Auto-Skill |
|-------------|------|-------|-------|-------|------|------------|
| typo_fix | Minimal | 1 | <10 | No | No | `quick` |
| rename_refactor | Low | ≤5 | Any | No | No | `quick` |
| bug_fix | Medium | Any | Any | Yes | No | `implementation` |
| feature_addition | High | Any | Any | Yes | No | `implementation` |
| architecture_change | Critical | >10 | Any | Yes | Yes | `spec-workflow` |
