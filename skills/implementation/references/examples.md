# Implementation Examples

## Example 1: Feature Implementation (TDD)

**Scenario**: Implement user authentication feature

**TDD Steps**:

### RED Phase - Write failing test
```bash
vic tdd red --test "User can login with valid credentials"
```

**Test Code**:
```javascript
// tests/auth.test.js
test('User can login with valid credentials', () => {
  const user = { email: 'test@example.com', password: 'password' };
  const result = authService.login(user);
  expect(result.success).toBe(true);
  expect(result.token).toBeDefined();
});
```

### GREEN Phase - Make test pass
```bash
vic tdd green --test "User can login with valid credentials" --passed
```

**Implementation**:
```javascript
// src/auth/authService.js
exports.login = (user) => {
  const userRecord = users.find(u => u.email === user.email);
  if (!userRecord || userRecord.password !== user.password) {
    return { success: false, error: 'Invalid credentials' };
  }
  const token = generateToken(userRecord.id);
  return { success: true, token };
};
```

### REFACTOR Phase - Improve code
```bash
vic tdd refactor
```

**Refactored Code**:
```javascript
// src/auth/authService.js
exports.login = async (user) => {
  const userRecord = await findByEmail(user.email);
  if (!userRecord || !await verifyPassword(user.password, userRecord.password)) {
    return { success: false, error: 'Invalid credentials' };
  }
  const token = generateToken(userRecord.id);
  return { success: true, token };
};
```

## Example 2: Bug Fix (Systematic Debugging)

**Scenario**: Fix intermittent API timeout

**Debug Steps**:

### Step 1: Start Debug Session
```bash
vic debug start --problem "API timeout occurs intermittently"
```

### Step 2: Survey - Gather Evidence
```bash
vic debug survey
```

**Evidence Collected**:
- Error occurs at 2:00 PM daily
- Only affects /api/users endpoint
- Database shows normal load
- Network latency spikes observed

### Step 3: Pattern - Find Similar Issues
```bash
vic debug pattern
```

**Similar Issues Found**:
- Issue #123: Similar timeout with /api/orders
- Issue #456: Connection pool exhaustion

### Step 4: Hypothesis - Form and Test
```bash
vic debug hypothesis --explain "Database connection pool exhausted during peak hours"
```

**Test**:
```javascript
// src/database/connectionPool.js
console.log('Active connections:', pool.all.length);
console.log('Max connections:', pool.max);
```

### Step 5: Implement Fix
```bash
vic debug implement --fix "Increase connection pool size" --root-cause "Pool size too small for peak load"
```

**Fix Applied**:
```javascript
// src/database/connectionPool.js
const pool = mysql.createPool({
  connectionLimit: 50, // Increased from 20
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
});
```

## Example 3: SPEC Alignment Check

**Scenario**: Verify code matches SPEC

**Command**:
```bash
vic spec gate 2
```

**Gate 2 Output**:
```
Gate 2: Code Alignment Check
=================================
✓ User registration endpoint implemented
✓ Password hashing implemented
✓ Email validation implemented
✗ Missing: Two-factor authentication
✗ Incomplete: Password reset flow
```

**Fix Alignment**:
```javascript
// Add missing TFA
exports.enableTFA = (userId) => {
  // TFA implementation
};

// Complete password reset
exports.resetPassword = (token, newPassword) => {
  // Complete reset flow implementation
};
```

## Example 4: Running Tests

**Scenario**: Ensure test coverage

**Commands**:
```bash
# Run Gate 3 - Test coverage check
vic spec gate 3

# Run specific tests
npm test -- --testPathPattern=auth

# Run integration tests
npm run test:integration
```

**Test Output**:
```
Test Suite Summary
===================
✓ Unit tests: 95% coverage
✓ Integration tests: 88% coverage
✗ E2E tests: 65% coverage (critical)
```

## Example 5: AI Slop Cleanup

**Scenario**: Remove AI-generated code issues

**Command**:
```bash
vic slop scan
```

**Issues Found**:
```
AI Slop Issues Found:
1. Long function > 100 lines
2. Magic numbers in code
3. Duplicate code blocks
4. Missing error handling
```

**Apply Fixes**:
```bash
vic slop fix --dry-run=false
```

**Fixed Code**:
```javascript
// Before: Long function
function processUserData(users) {
  // ... 150 lines of code
}

// After: Extracted functions
function validateUser(user) {
  // User validation logic
}

function transformUserData(user) {
  // Data transformation logic
}

function processUserData(users) {
  return users.map(user => {
    if (!validateUser(user)) return null;
    return transformUserData(user);
  }).filter(Boolean);
}
```