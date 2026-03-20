# QA Skill

## Overview

Combines vibe-qa + spec-driven-test + test-driven-development for quality assurance.

**When to use:**
- Before claiming "done"
- After implementing a feature
- Before releasing

## Test Pyramid

```
         E2E      ← QA tests (Playwright)
      Integration   ← spec-driven tests
        Unit Tests  ← TDD tests
```

## Mode 1: Test-Driven Development

### Red-Green-Refactor Cycle

```bash
# RED: Write failing test
vic tdd red --test "should validate email"

# GREEN: Write minimal code to pass
vic tdd green --test "should validate email" --passed

# REFACTOR: Improve code
vic tdd refactor
```

### TDD Rules

1. Never write code without a failing test
2. Write only enough code to pass the test
3. Refactor to improve structure

## Mode 2: Spec-Driven Testing

### From Contracts to Tests

```javascript
// contract.json defines:
POST /api/users { email, name } → { id, email, name }

// Test:
describe('POST /api/users', () => {
  it('creates user with email and name', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
    expect(res.status).toBe(201)
    expect(res.body).toMatchObject({ email: 'test@example.com' })
  })
  
  it('returns 400 for invalid email', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', name: 'Test' })
    expect(res.status).toBe(400)
  })
})
```

## Mode 3: E2E Testing (Playwright)

```bash
# Initialize
vic qa init

# Quick smoke test
vic qa quick

# Full test
vic qa full

# Screenshot
vic qa screenshot --name "login-page"
```

## Gate 3: Test Coverage Check

`vic spec gate 3` validates:
- Test files exist
- Test framework configured
- Key modules have tests
- Critical paths covered

## Verification Checklist

Before claiming done:
- [ ] `vic spec gate 3` passes
- [ ] All TDD tests pass
- [ ] E2E tests pass
- [ ] No regression in existing tests

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `spec-architect` | Contracts drive test generation |
| `debugging` | Fix failing tests |
| `sdd-orchestrator` | Phase gate enforcement |
