---
name: test-driven-development
description: Use when you need to develop single-module logic through the red-green-refactor cycle, or when the project does not have SPEC/contract infrastructure yet.
---

# Test-Driven Development (TDD)

## Overview

TDD is a **standalone development mode** — NOT part of the SDD pipeline. Use it when:
- Project has no SPEC/contract infrastructure
- Working on single-module internal logic
- Exploring an algorithm or data structure
- Writing unit tests for existing untested code (test-after)

**Core cycle: Red → Green → Refactor**

## TDD vs SDD

| Dimension | TDD | SDD |
|-----------|-----|-----|
| **Scope** | Single module / function | Multi-module / cross-service |
| **Interface** | None (internal logic) | Explicit contracts |
| **Tests** | Unit tests (any level) | Contract verification tests |
| **Test-first** | Yes (red-green) | No (spec-first) |
| **Traceability** | Test → Code | SPEC → Contract → Code → Test |
| **Gateway** | None | Formal gates |
| **When to use** | Single file, algorithm, internal logic | System features, APIs, cross-module |

## When to Use TDD

**Use when ALL conditions are met:**
1. Project has NO `.vic-sdd/SPEC-REQUIREMENTS.md` (or this is a separate module)
2. Working on internal implementation (no cross-module interfaces)
3. The task is a single function, algorithm, or data transformation
4. User did NOT ask for contracts, APIs, or cross-service work
5. Complexity is in logic/algorithm, not in requirement clarification

**Use SDD instead when:**
- User mentions API, interface, contract, or cross-module work
- Project has existing SPEC/contract infrastructure
- Task involves multiple services or databases
- Compliance/traceability requirements exist

## The Red-Green-Refactor Cycle

### Step 1: RED — Write a failing test

```
Write the smallest possible test that describes the behavior you want.
The test MUST fail — it describes what SHOULD happen, not what happens.
```

Rules:
- Write ONE assertion at a time
- Name test clearly: [method]_[scenario]_[expected result]
- Do NOT write implementation code yet

Example:
```typescript
// auth.test.ts
describe('hashPassword', () => {
  it('should return a hash of length 64 for any input', () => {
    const hash = hashPassword('password123');
    expect(hash).toHaveLength(64); // SHA-256 hex
  });
});
```

### Step 2: GREEN — Make it pass

```
Write the minimum code needed to make the test pass.
DO NOT optimize yet — just make it work.
```

Rules:
- Write only what the test expects
- No extra features
- No optimization (that comes in Refactor)

Example:
```typescript
function hashPassword(password: string): string {
  return crypto.createHash('sha256').update(password).digest('hex');
}
```

### Step 3: REFACTOR — Improve without breaking tests

```
Now that tests pass, improve the code.
Keep all tests green while improving design.
```

Rules:
- Extract functions
- Reduce duplication
- Improve naming
- All tests must remain green

## Test Naming Convention

```
[Unit]_[Scenario]_[Expected Result]

Examples:
- parseMarkdown_toHTML_handlesBoldText
- validateEmail_returnsFalseForInvalidFormat
- calculateDiscount_appliesToOrdersOver100
- TokenService_generateToken_includesExpiry
```

## Test Structure

### Arrange-Act-Assert (AAA)

```typescript
describe('UnitName', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [scenario]', () => {
      // Arrange
      const input = createTestInput();
      const mock = createMock();

      // Act
      const result = methodUnderTest(input, mock);

      // Assert
      expect(result).toEqual(expectedOutput);
    });
  });
});
```

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Writing implementation before test | Defeats TDD purpose | Write test first, always |
| Writing too many tests at once | Loses small-step benefit | One test at a time |
| Testing private methods | Fragile, tests implementation not behavior | Test public behavior |
| Asserting too much in one test | Unclear failure reason | One assertion per test |
| Skipping refactor step | Code rots over time | Always refactor while green |
| Not naming tests clearly | Can't understand what failed | Follow naming convention |
| Mocking everything | Tests don't reflect reality | Mock only external dependencies |

## Integration with VIC-SDD

### Trigger Points

1. **User request does not mention SPEC/contracts** → Check if TDD is appropriate
2. **Single-module refactor** → Use TDD for internal logic
3. **Algorithm exploration** → Use TDD red-green cycle
4. **Existing untested code** → Use test-after mode

### Layered Mode (SDD + TDD Together)

When working in SDD mode, TDD applies ONLY to internal implementation:

```
SDD Layer (Contract):
  - Test cross-module interfaces via spec-driven-test
  - All public APIs have contract coverage
  - Changes to contracts go through spec-contract-diff

TDD Layer (Internal):
  - Internal logic via red-green-refactor
  - Unit tests for functions not exposed externally
  - TDD tests do NOT reference contract structure
  - TDD tests live in same directory as code, NOT in .sdd-spec/
```

**Rule: TDD tests and SDD contract tests NEVER overlap in scope.**

## Invocation Examples

```bash
# Activate TDD mode
skill test-driven-development
# "Implement a rate limiter using TDD"

# When exploring an algorithm
skill test-driven-development
# "Help me explore different sorting algorithms with TDD"

# When adding unit tests to existing code
skill test-driven-development
# "Add TDD unit tests for the auth module"
```

## Quick Reference

| Phase | Action | Output |
|-------|--------|--------|
| RED | Write failing test | Compiler error or test failure |
| GREEN | Write minimal implementation | Tests pass |
| REFACTOR | Improve code | Tests still pass |

| Decision Point | Answer | Mode |
|----------------|--------|------|
| Cross-module interface? | Yes | SDD |
| Has SPEC/contracts? | Yes | SDD |
| Single function/algorithm? | Yes | TDD |
| No SPEC infrastructure? | Yes | TDD |
| Algorithm complexity? | High | TDD |

---

## Pipeline Metadata

pipeline_metadata:
  handoff:
    delivers:
      - artifact: "test files (*.test.*)"
        description: "Executable unit tests in red-green-refactor cycle"
      - artifact: "implementation code"
        description: "Production code that passes all tests"
    consumes:
      - artifact: "feature description"
        description: "What behavior to implement"
      - artifact: "existing codebase (optional)"
        description: "Context for test-after mode"
  exit_condition:
    success: "All tests green, code refactored, no failing tests"
    failure: "Test perpetually fails — reconsider design or scope"
    triggers_next_on_success: "vibe-qa (e2e verification) or commit"
    triggers_next_on_failure: "vibe-debug (root cause) or spec-architect (switch to SDD)"
  agent_pattern: Generator
