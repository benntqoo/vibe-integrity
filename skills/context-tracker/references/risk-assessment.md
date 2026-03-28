# Risk Assessment

> Risk level evaluation for intelligent workflow selection

## Overview

Risk assessment evaluates the potential impact of changes to determine the appropriate level of quality gates and workflow strictness.

## Risk Factors

### 1. Scope (影响范围)

| Score | Level | Description | Examples |
|-------|-------|-------------|----------|
| 1 | Single File | Change affects one file | typo fix, comment update |
| 2 | Single Module | Change affects one module/feature | bug fix in one service |
| 3 | Multiple Modules | Change affects multiple modules | API change affecting frontend + backend |
| 4 | Cross-cutting | Change affects entire system | authentication refactor, database migration |

**Detection:**
```bash
# Count affected files
FILE_COUNT=$(git diff --name-only | wc -l)

# Check module spread
MODULES=$(git diff --name-only | cut -d'/' -f1-2 | sort -u | wc -l)

# Score mapping
if [ $FILE_COUNT -eq 1 ]; then SCOPE=1
elif [ $MODULES -eq 1 ]; then SCOPE=2
elif [ $MODULES -le 3 ]; then SCOPE=3
else SCOPE=4
fi
```

---

### 2. Complexity (复杂度)

| Score | Level | Description | Indicators |
|-------|-------|-------------|------------|
| 1 | Trivial | Obvious, mechanical change | typo, rename, formatting |
| 2 | Simple | Straightforward change | add validation, update config |
| 3 | Moderate | Requires understanding | new endpoint, refactor function |
| 4 | Complex | Requires deep understanding | new architecture, algorithm change |

**Detection:**
```bash
# Check for complex patterns
COMPLEX_PATTERNS=$(git diff --unified=0 | grep -cE "(async|await|Promise|thread|lock|transaction)")

# Check nesting depth change
NESTING_CHANGE=$(git diff --unified=0 | grep -cE "^\+.*{.*{.*{")

# Check for new abstractions
NEW_ABSTRACTIONS=$(git diff --unified=0 | grep -cE "^\+.*(interface|abstract|protocol)")

# Simplified scoring
if [ $COMPLEX_PATTERNS -eq 0 ] && [ $NEW_ABSTRACTIONS -eq 0 ]; then
  COMPLEXITY=1
elif [ $NEW_ABSTRACTIONS -gt 0 ]; then
  COMPLEXITY=4
elif [ $COMPLEX_PATTERNS -gt 3 ]; then
  COMPLEXITY=3
else
  COMPLEXITY=2
fi
```

---

### 3. SPEC Impact (SPEC 影响度)

| Score | Level | Description | Examples |
|-------|-------|-------------|----------|
| 0 | None | No SPEC changes needed | internal refactor, typo fix |
| 1 | Minor | Small SPEC clarification | add edge case, update example |
| 2 | Moderate | SPEC section update | new parameter, behavior change |
| 3 | Major | SPEC restructuring | new feature, breaking change |

**Detection:**
```bash
# Check if SPEC files are affected
SPEC_AFFECTED=$(git diff --name-only | grep -cE "SPEC-.*\.md|\.vic-sdd/")

# Check for SPEC-related keywords
SPEC_KEYWORDS=$(echo "$TASK_DESCRIPTION" | grep -ciE "spec|requirement|contract|api|interface")

if [ $SPEC_AFFECTED -gt 0 ]; then
  SPEC_IMPACT=3
elif [ $SPEC_KEYWORDS -gt 0 ]; then
  SPEC_IMPACT=2
elif [ $SCOPE -gt 2 ]; then
  SPEC_IMPACT=1
else
  SPEC_IMPACT=0
fi
```

---

### 4. Test Coverage (测试覆盖需求)

| Score | Level | Description | Action |
|-------|-------|-------------|--------|
| 0 | Existing Sufficient | Current tests cover change | No new tests needed |
| 1 | Needs Update | Existing tests need update | Update test assertions |
| 2 | Needs New Tests | New test cases needed | Add unit tests |
| 3 | Needs Integration | Integration tests needed | Add E2E/integration tests |

**Detection:**
```bash
# Check if test files changed
TEST_FILES_CHANGED=$(git diff --name-only | grep -cE "(test|spec)_" || echo 0)

# Check for new functions that need tests
NEW_FUNCTIONS=$(git diff --unified=0 | grep -cE "^\+.*(function|def|export)")

# Check for integration patterns
INTEGRATION_PATTERNS=$(git diff --unified=0 | grep -cE "(api|endpoint|route|handler)")

if [ $TEST_FILES_CHANGED -gt 0 ] && [ $NEW_FUNCTIONS -eq 0 ]; then
  TEST_COVERAGE=0
elif [ $NEW_FUNCTIONS -gt 0 ] && [ $INTEGRATION_PATTERNS -eq 0 ]; then
  TEST_COVERAGE=2
elif [ $INTEGRATION_PATTERNS -gt 0 ]; then
  TEST_COVERAGE=3
elif [ $TEST_FILES_CHANGED -gt 0 ]; then
  TEST_COVERAGE=1
else
  TEST_COVERAGE=0
fi
```

---

## Risk Calculation

### Formula

```
risk_score = (scope + complexity + spec_impact + test_coverage) / 4

where:
  scope ∈ [1, 4]
  complexity ∈ [1, 4]
  spec_impact ∈ [0, 3]
  test_coverage ∈ [0, 3]

risk_score ∈ [0.25, 3.5]
```

### Normalized Score

```
normalized_risk = (risk_score - 0.25) / (3.5 - 0.25) × 4

normalized_risk ∈ [0, 4]
```

---

## Risk Levels

### Level Definitions

| Level | Score | Description | Workflow |
|-------|-------|-------------|----------|
| **Minimal** | 0.0 - 1.0 | Trivial, low impact | `quick`, no gates |
| **Low** | 1.0 - 2.0 | Simple, contained | `quick`, optional gate_2 |
| **Medium** | 2.0 - 2.75 | Moderate complexity | `implementation`, gate_2 + gate_3 |
| **High** | 2.75 - 3.5 | Significant impact | `implementation`, all gates |
| **Critical** | 3.5 - 4.0 | Major change, high risk | `spec-workflow` + `implementation`, all gates + checkpoint |

### Gate Selection Matrix

| Risk Level | Gate 0 | Gate 1 | Gate 2 | Gate 3 | Human Checkpoint |
|------------|--------|--------|--------|--------|------------------|
| Minimal | ⏭️ Skip | ⏭️ Skip | ⏭️ Skip | ⏭️ Skip | ❌ No |
| Low | ⏭️ Skip | ⏭️ Skip | ⚡ Optional | ⏭️ Skip | ❌ No |
| Medium | ⏭️ Skip | ⏭️ Skip | ✅ Required | ✅ Required | ❌ No |
| High | ✅ Required | ⏭️ Skip | ✅ Required | ✅ Required | ⚠️ Optional |
| Critical | ✅ Required | ✅ Required | ✅ Required | ✅ Required | ✅ Required |

---

## Examples

### Example 1: Typo Fix

```yaml
task: "Fix typo in README.md"

assessment:
  scope: 1          # Single file
  complexity: 1     # Trivial
  spec_impact: 0    # None
  test_coverage: 0  # None

risk_score: (1 + 1 + 0 + 0) / 4 = 0.5
risk_level: Minimal

workflow:
  skill: quick
  gates: []
  checkpoint: false
```

### Example 2: Bug Fix

```yaml
task: "Fix login validation bug"

assessment:
  scope: 2          # Single module (auth)
  complexity: 2     # Simple logic fix
  spec_impact: 0    # No SPEC change
  test_coverage: 2  # Need new test

risk_score: (2 + 2 + 0 + 2) / 4 = 1.5
risk_level: Low-Medium

workflow:
  skill: implementation
  gates: [gate_2, gate_3]
  checkpoint: false
```

### Example 3: New Feature

```yaml
task: "Add user profile API"

assessment:
  scope: 3          # Multiple modules (API, DB, Auth)
  complexity: 3     # Moderate (new endpoints, models)
  spec_impact: 2    # SPEC section update
  test_coverage: 3  # Integration tests needed

risk_score: (3 + 3 + 2 + 3) / 4 = 2.75
risk_level: High

workflow:
  skill: implementation
  gates: [gate_0, gate_2, gate_3]
  checkpoint: optional
```

### Example 4: Architecture Change

```yaml
task: "Migrate from REST to GraphQL"

assessment:
  scope: 4          # Cross-cutting
  complexity: 4     # Complex
  spec_impact: 3    # Major SPEC restructure
  test_coverage: 3  # Integration tests needed

risk_score: (4 + 4 + 3 + 3) / 4 = 3.5
risk_level: Critical

workflow:
  skill: spec-workflow → implementation
  gates: [gate_0, gate_1, gate_2, gate_3]
  checkpoint: required
```

---

## Vic Commands

```bash
# Assess current changes
vic assess --risk

# Output:
# Risk Assessment
# ===============
# Scope: 2 (Single Module)
# Complexity: 3 (Moderate)
# SPEC Impact: 1 (Minor)
# Test Coverage: 2 (Needs New Tests)
#
# Risk Score: 2.0
# Risk Level: Medium
#
# Gates Required: [gate_2, gate_3]
# Checkpoint: Not required
```

---

## Summary

| Factor | Range | Weight | Detection |
|--------|-------|--------|-----------|
| Scope | 1-4 | 25% | File/module count |
| Complexity | 1-4 | 25% | Pattern analysis |
| SPEC Impact | 0-3 | 25% | SPEC file changes |
| Test Coverage | 0-3 | 25% | Test file analysis |

**Risk Score** = Average of all factors

**Risk Level** = Mapped from score range
