# Escalation Criteria

## Overview

Quick workflow is designed for simple, single-file changes. When a task exceeds these boundaries, it must be escalated to the appropriate skill. This document outlines when and how to escalate.

## When to Escalate

### 1. Multi-File Changes

**Trigger**: Changes affect more than one file

**Examples**:
- Modifying a component and its test file
- Updating API and related documentation
- Changing shared utilities and their consumers

**Symptoms**:
```bash
# Multiple files in git diff
git diff --name-only | wc -l > 1

# Files across directories
git diff --name-only | grep -E "src/|tests/|docs/" | head -5
```

**Correct Escalation**:
```bash
# Escalate to implementation skill
vic implementation

# Or use TDD for new features
vic tdd start --feature "new-feature"
```

### 2. SPEC Impact

**Trigger**: Changes affect requirements or architecture

**Examples**:
- New API endpoints
- Business logic changes
- Data model modifications

**Detection Methods**:
```bash
# Check SPEC files
git diff --name-only | grep "SPEC-.*\.md"

# Run SPEC alignment check
vic spec gate 2
```

**Correct Escalation**:
```bash
# Use spec-workflow for requirements changes
vic spec-workflow

# Or create/update SPEC
vic spec init
```

### 3. Test Requirements

**Trigger**: Need to write tests for the changes

**Examples**:
- New functionality requires testing
- Bug fix needs regression tests
- Coverage requirements

**Detection**:
```bash
# Test files needed
if [ "$NEEDS_TESTS" = "true" ]; then
  echo "Need tests"
fi

# Coverage threshold
npm test -- --coverage --watchAll=false
```

**Correct Escalation**:
```bash
# Use implementation skill for TDD
vic implementation

# Or start with TDD
vic tdd start --feature "feature-name"
```

### 4. Complex Logic

**Trigger**: Adding complex algorithms or business logic

**Examples**:
- Complex calculations
- State management
- Performance-critical code

**Detection Methods**:
```javascript
// Complex function indicators
function complexFunction(data) {
  // Multiple nested conditions
  if (condition1) {
    if (condition2) {
      // Deep nesting
      if (condition3) {
        // More logic...
      }
    }
  }

  // Multiple loops
  for (let i = 0; i < data.length; i++) {
    for (let j = 0; j < data[i].length; j++) {
      // Nested processing
    }
  }
}
```

**Correct Escalation**:
```bash
# Use implementation with systematic debugging
vic implementation

# Or use debugging process
vic debug start --problem "complex logic implementation"
```

### 5. Architecture Changes

**Trigger**: Changes to system architecture or patterns

**Examples**:
- New design patterns
- Technology stack changes
- Significant refactoring

**Detection**:
```bash
# Architecture indicators
grep -r "new Architecture" src/
grep -r "deprecated" src/
```

**Correct Escalation**:
```bash
# Use spec-workflow for architecture
vic spec-workflow

# Or design review
vic design-review
```

## Escalation Process

### Step 1: Detect Trigger
Monitor for escalation triggers during development:
```bash
# Check for multi-file changes
git diff --name-only | wc -l

# Check SPEC impact
vic spec diff

# Run diagnostics
vic check --all
```

### Step 2: Choose Right Skill
Map triggers to appropriate skills:
```
Multi-File + Tests → implementation
SPEC Impact → spec-workflow
Architecture → spec-workflow
Complex Logic → implementation
Unclear Requirements → spec-workflow
```

### Step 3: Escalate Command
Use the appropriate escalation command:
```bash
# Escalate to implementation
vic implementation

# Escalate to spec-workflow
vic spec-workflow

# Escalate to unified-workflow
vic unified-workflow
```

### Step 4: Handover Process
When escalating, provide context:
```bash
# Include current changes
git add .
git commit -m "WIP: changes before escalation"

# Document decision
echo "Escalated from quick to implementation due to multi-file changes" >> .vic-sdd/notes.md
```

## Escalation Command Reference

### Quick to Implementation
```bash
# Escalate with reason
vic implementation --from-quick --reason "multi-file changes needed"

# Continue current work
git stash
vic implementation
git stash pop
```

### Quick to SPEC Workflow
```bash
# For requirements changes
vic spec-workflow --from-quick --reason "new requirements detected"

# Update SPEC based on changes
vic spec init --update
```

### Quick to Unified Workflow
```bash
# For workflow management
vic unified-workflow --from-quick --reason "phase advancement needed"

# Check current state
vic status
```

## Prevention Strategies

### 1. Plan Before Starting
```bash
# Estimate scope before starting
echo "Files to change:"
echo "- README.md (typo fix)"
echo "- No other files affected"

# Confirm with team
echo "Confirmed: single-file change, safe for quick workflow"
```

### 2. Use Dry Runs
```bash
# Preview changes
git diff --name-only

# Check impact
vic deps impact <module>
```

### 3. Regular Checkpoints
```bash
# After making changes
git status

# Before committing
vic gate check --blocking
```

### 4. Documentation
```markdown
# In pull description
## Quick Workflow Checklist
- [ ] Single file only
- [ ] No SPEC impact
- [ ] No new tests
- [ ] Minimal change
- [ ] Verified no LSP errors
```

## Common Escalation Scenarios

### Scenario 1: "Just a small fix"
**Problem**: Underestimated scope

**Solution**:
```bash
# Before starting
echo "Files affected:"
git diff --name-only

# After first change
git add file1.js
echo "Now check if more changes needed..."
```

### Scenario 2: "One more thing"
**Problem**: Scope creep

**Solution**:
```bash
# Each change must be evaluated
echo "Change: add logging"
echo "Scope: single file?"
echo "Impact: new requirements?"
echo "Decision: [quick|implementation]"
```

### Scenario 3: "Need to match style"
**Problem**: Refactoring for consistency

**Solution**:
```bash
# If style changes affect multiple files
echo "Style changes affect:"
grep -r "old-style" src/
echo "Escalate to implementation for refactoring"
```

## Monitoring and Metrics

### Track Escalations
```bash
# Count escalations per week
git log --oneline --grep="escalation" --since="1 week ago" | wc -l

# Common escalation reasons
git log --oneline --grep="from quick" | grep -oE -- '--reason "[^"]*"' | sort | uniq -c
```

### Metrics to Monitor
1. **Escalation Rate**: % of tasks that escalate
2. **Time to Escalation**: How long before escalation needed
3. **Common Triggers**: Which triggers cause most escalations
4. **Skill Distribution**: Which skills are most often needed after quick

### Improve Process
Based on metrics:
```bash
# If multi-file is common trigger
echo "Add multi-file check to quick workflow script"

# If SPEC impact is common
echo "Add SPEC diff check to quick workflow"
```

## Emergency Escalation

### When Quick Becomes Critical
```bash
# Immediate escalation
vic implementation --emergency --reason "production issue"

# Skip current work
git stash
```

### Rollback Plan
```bash
# If quick change causes issue
git reset --hard HEAD~1

# Escalate properly
vic debug start --problem "quick workflow failure"
```

Remember: Quick workflow is for simple changes. When in doubt, escalate!