---
name: spec-test
description: Use when implementing any feature or bugfix - enforces TDD methodology with Red-Green-Refactor cycle.
---

# Spec Test - TDD Enforcement

**Iron Law: Never write implementation code until a test fails first.**

---

## When to Use

**Use when:**
- Writing new feature code
- Fixing bugs
- Refactoring existing code
- Any implementation work

**NOT use when:**
- Reading or understanding code
- Design discussions
- Documentation only

---

## The Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────┐
│                    TDD Cycle                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐           │
│   │   RED   │ ──▶ │  GREEN  │ ──▶ │ REFACTOR│           │
│   │  Write  │     │  Make   │     │ Improve │           │
│   │ Failing │     │   It    │     │   It    │           │
│   │  Test   │     │  Pass   │     │         │           │
│   └─────────┘     └─────────┘     └─────────┘           │
│       │               │               │                  │
│       └───────────────┴───────────────┘                  │
│                    (Repeat)                              │
└─────────────────────────────────────────────────────────┘
```

### Phase 1: RED - Write a Failing Test

```bash
# 1. Write test for the behavior you want
# 2. Run test - it MUST fail
# 3. Verify failure message is clear

npm test
# Expected: FAIL - Test fails because implementation doesn't exist yet
```

### Phase 2: GREEN - Make It Pass

```bash
# 1. Write MINIMUM code to pass the test
# 2. No optimization, no "what ifs"
# 3. Run test - it MUST pass
# 4. All previous tests still pass

npm test
# Expected: PASS - Implementation works
```

### Phase 3: REFACTOR - Improve

```bash
# 1. Improve code structure
# 2. Remove duplication
# 3. Improve naming
# 4. Run tests - ALL must still pass

npm test
# Expected: PASS - Refactoring didn't break anything
```

---

## TDD Rules

| Rule | Description |
|------|-------------|
| No implementation without test | Tests come FIRST |
| One test at a time | Focus on current requirement |
| Minimal implementation | Just enough to pass |
| Tests are specs | If tested, it's documented |
| Green bar ASAP | Get to passing quickly |

---

## Test Coverage Requirements

| Feature Type | Minimum Coverage |
|--------------|------------------|
| API Endpoints | Integration tests |
| Business Logic | Unit tests |
| UI Components | Component tests |
| Critical Flows | E2E tests |

---

## TDD in VIBE-SDD Workflow

```
定图纸 → 打地基 → 立规矩
    │          │         │
    ▼          ▼         ▼
 Gate 0    Gate 1    TDD Loop
                            │
                            ▼
                    ┌───────────────┐
                    │ Write Failing│
                    │     Test     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Implement to  │
                    │  Make Pass    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Refactor   │
                    │  (if needed) │
                    └───────┬───────┘
                            │
                            ▼
                      Gate 3
                    (Test Coverage)
```

---

## Quick Reference

| Phase | Command | Goal |
|-------|---------|------|
| RED | `npm test` (before impl) | Verify test fails |
| GREEN | `npm test` (after impl) | Verify test passes |
| REFACTOR | `npm test` (after refactor) | Verify nothing broke |

| VIC Command | Purpose |
|-------------|---------|
| `vic tdd start` | Start TDD session |
| `vic tdd status` | Show current TDD state |
| `vic tdd checkpoint` | Save TDD progress |
| `vic slop scan` | Detect AI slop in tests |

---

## Common Mistakes

| Mistake | TDD Correct Approach |
|---------|---------------------|
| Writing impl before test | Always write test FIRST |
| Testing implementation details | Test behavior, not structure |
| Large tests | One assertion per test |
| Skipping refactor | Refactor AFTER green |
| Not running all tests | Run full suite frequently |

---

## Example TDD Session

```
User Story: "As a user, I can calculate tip"

AI (RED Phase):
# Create test first
test("calculate tip - 15%", () => {
  expect(calculateTip(100, 0.15)).toBe(15);
});

$ npm test
> FAIL: calculateTip is not defined ✅

AI (GREEN Phase):
# Minimal implementation
function calculateTip(amount, percent) {
  return amount * percent;
}

$ npm test
> PASS ✅

AI (REFACTOR Phase):
# Already minimal, ready for next test
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `vibe-debug` | Use when tests fail unexpectedly |
| `spec-architect` | Tests validate acceptance criteria |
| `vibe-qa` | E2E tests verify user flows |

---

**Remember: Red → Green → Refactor → Repeat**

Never break the cycle. Tests are the safety net that enables confident refactoring.
