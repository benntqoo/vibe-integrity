# TDD Guide

> Test-Driven Development workflow for VIBE-SDD

## Overview

TDD (Test-Driven Development) is a development approach where tests are written **before** the implementation code. This ensures code correctness and maintainability.

## TDD Cycle

```
🔴 RED → 🟢 GREEN → 🔵 REFACTOR → (repeat)
  Write    Make it     Improve
  failing   pass      code
  test
```

## Phase Details

### 🔴 RED Phase

**Purpose**: Write a failing test that defines expected behavior.

**Steps**:
1. Identify the feature or behavior to implement
2. Write a test that describes the expected outcome
3. Run the test - it must FAIL
4. If test passes, the test is wrong

**Example**:
```javascript
// Test for user validation
describe('validateUser', () => {
  it('should reject invalid email', () => {
    const result = validateUser({ email: 'invalid' });
    expect(result.valid).toBe(false);
  });
});
```

**Vic Command**:
```bash
vic tdd red --test "should reject invalid email"
```

### 🟢 GREEN Phase

**Purpose**: Write the **minimal** code to make the test pass.

**Rules**:
- Write only enough code to pass the test
- Do NOT refactor or optimize
- Do NOT add extra features
- Hardcoded values are acceptable if they make the test pass

**Example**:
```javascript
function validateUser(user) {
  if (!user.email.includes('@')) {
    return { valid: false };
  }
  return { valid: true };
}
```

**Vic Command**:
```bash
vic tdd green --test "should reject invalid email" --passed
```

### 🔵 REFACTOR Phase

**Purpose**: Improve code quality while keeping tests green.

**Activities**:
- Remove duplication
- Improve naming
- Extract functions
- Simplify logic
- Add constants for magic numbers

**Rules**:
- Tests must stay GREEN after each change
- Refactor in small steps
- Run tests after each change

**Example**:
```javascript
// Before refactor
function validateUser(user) {
  if (!user.email.includes('@')) {
    return { valid: false };
  }
  return { valid: true };
}

// After refactor
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateUser(user) {
  return {
    valid: EMAIL_REGEX.test(user.email)
  };
}
```

**Vic Command**:
```bash
vic tdd refactor
```

## TDD Best Practices

### 1. Test First, Always
- Never write implementation before test
- If you find a bug, write a failing test first

### 2. One Assertion Per Test
```javascript
// Good
it('should validate email format', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
});

// Avoid
it('should validate email', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
  expect(isValidEmail('invalid')).toBe(false);
  expect(isValidEmail('')).toBe(false);
});
```

### 3. Descriptive Test Names
```javascript
// Good
it('should return false when email lacks @ symbol', () => {...});

// Avoid
it('test1', () => {...});
```

### 4. Test Behavior, Not Implementation
```javascript
// Good - tests behavior
it('should format currency with symbol', () => {
  expect(formatCurrency(100, 'USD')).toBe('$100.00');
});

// Avoid - tests implementation
it('should call toLocaleString', () => {
  const spy = jest.spyOn(Number.prototype, 'toLocaleString');
  formatCurrency(100, 'USD');
  expect(spy).toHaveBeenCalled();
});
```

### 5. Keep Tests Independent
- Each test should run in isolation
- No shared state between tests
- Use beforeEach/afterEach for setup/teardown

## TDD Workflow with Vic

### Starting a TDD Session
```bash
vic tdd start --feature "user authentication"
```

### During Development
```bash
# Write failing test
vic tdd red --test "should hash password with bcrypt"

# Make it pass
vic tdd green --test "should hash password with bcrypt" --passed

# Refactor
vic tdd refactor

# Check status
vic tdd status
```

### Checkpoint
```bash
vic tdd checkpoint --note "Password hashing complete"
```

### History
```bash
vic tdd history
```

## Test Categories

### Unit Tests
- Test single functions/methods
- Mock all dependencies
- Fast execution

### Integration Tests
- Test component interactions
- Use real or mock databases
- Medium speed

### E2E Tests
- Test complete user flows
- Use real environment
- Slow execution

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| Skipping RED phase | Always write failing test first |
| Writing too much code in GREEN | Write minimal code only |
| Refactoring without tests | Ensure tests exist and pass first |
| Testing implementation | Focus on behavior testing |
| Large tests | Break into smaller, focused tests |

## Test Coverage Targets

| Type | Target | Command |
|------|--------|---------|
| Unit Tests | 90%+ | `vic spec gate 3` |
| Integration Tests | 80%+ | `npm run test:integration` |
| E2E Tests | Critical paths | `vic qa full` |

## Integration with SDD

TDD integrates with SDD gates:

1. **After TDD cycle**: Run `vic spec gate 2` to verify code aligns with SPEC
2. **Before commit**: Run `vic spec gate 3` to verify test coverage
3. **During refactoring**: Use `vic slop scan` to detect code quality issues

## Summary

| Phase | Goal | Key Action |
|-------|------|------------|
| RED | Define behavior | Write failing test |
| GREEN | Make it work | Write minimal code |
| REFACTOR | Make it clean | Improve without breaking |

Remember: **RED → GREEN → REFACTOR** is a cycle, not a one-time process. Repeat as needed.
