# Traceability Patterns

## Overview

Traceability ensures that requirements flow through to implementation and testing. These patterns help maintain clear links between user stories, specifications, code, and tests.

## Core Traceability Chain

```
User Story → SPEC Contract → Code → Tests
```

## Pattern 1: Direct Implementation Trace

**Description**: One-to-one mapping between requirement and implementation

**Structure**:
```
User Story
├── SPEC-REQ-001
├── src/feature/module.js
└── tests/feature/module.test.js
```

**Example**:

### User Story
```markdown
### US-001: User Login
- As a user, I want to login with my credentials
- Acceptance Criteria:
  - Valid credentials grant access
  - Invalid credentials show error
  - Session is created on success
```

### SPEC Contract
```markdown
# SPEC-REQUIREMENTS.md

## REQ-US-001: User Authentication

### Login Function
- Endpoint: POST /api/auth/login
- Request: { email: string, password: string }
- Response: { success: boolean, token?: string, error?: string }
- Status codes: 200 (success), 401 (failed)
```

### Implementation
```javascript
// src/auth/authController.js
exports.login = async (req, res) => {
  const { email, password } = req.body;
  const user = await authService.authenticate(email, password);

  if (user) {
    const token = generateToken(user.id);
    res.json({ success: true, token });
  } else {
    res.status(401).json({ success: false, error: 'Invalid credentials' });
  }
};
```

### Tests
```javascript
// tests/auth.test.js
describe('User Login', () => {
  test('valid credentials grant access', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'password' });

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.token).toBeDefined();
  });

  test('invalid credentials show error', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'wrong@example.com', password: 'wrong' });

    expect(res.status).toBe(401);
    expect(res.body.success).toBe(false);
  });
});
```

## Pattern 2: Shared Implementation Trace

**Description**: Multiple requirements share common implementation

**Structure**:
```
User Story A → SPEC-REQ-A1
User Story B → SPEC-REQ-B1
Shared Implementation → src/shared/module.js
Tests A → tests/feature/a.test.js
Tests B → tests/feature/b.test.js
Shared Tests → tests/shared/module.test.js
```

**Example**:

### User Stories
```markdown
### US-002: Reset Password
- As a user, I want to reset my password via email

### US-003: Update Profile
- As a user, I want to update my profile information
```

### Shared Implementation
```javascript
// src/user/userService.js
class UserService {
  async updateProfile(userId, profile) {
    // Common validation logic
    this.validateUser(profile);

    // Common update pattern
    return this.updateUser(userId, profile);
  }

  async requestPasswordReset(email) {
    // Common email validation
    if (!this.validateEmail(email)) {
      throw new Error('Invalid email');
    }

    // Common notification pattern
    return this.sendNotification(email, 'password-reset');
  }
}
```

## Pattern 3: Component Traceability

**Description**: Traceability organized by components/modules

**Structure**:
```
Component: User Management
├── User Story: Register User (US-004)
├── User Story: Edit Profile (US-005)
├── SPEC: User Management.md
├── Implementation:
│   ├── src/user/userController.js
│   ├── src/user/userService.js
│   └── src/user/userModel.js
└── Tests:
    ├── tests/user/register.test.js
    ├── tests/user/edit.test.js
    └── tests/user/model.test.js
```

**Example**:

### Component SPEC
```markdown
# SPEC: User Management Component

## Overview
Handles user registration, profile management, and authentication

## Dependencies
- Database: PostgreSQL
- Cache: Redis
- Auth: JWT

## APIs
- POST /api/users/register
- PUT /api/users/:id
- GET /api/users/:id
```

### Component Implementation
```javascript
// src/user/userController.js
class UserController {
  async register(req, res) {
    const user = await userService.create(req.body);
    res.status(201).json(user);
  }

  async update(req, res) {
    const user = await userService.update(req.params.id, req.body);
    res.json(user);
  }

  async get(req, res) {
    const user = await userService.findById(req.params.id);
    res.json(user);
  }
}
```

## Pattern 4: Hierarchical Traceability

**Description**: Trace requirements at different levels (epic, feature, task)

**Structure**:
```
Epic: User Management (EPIC-001)
├── Feature: Authentication (FEAT-001)
│   ├── User Story: Login (US-001)
│   ├── User Story: Register (US-002)
│   └── User Story: Reset Password (US-003)
└── Feature: Profile Management (FEAT-002)
    ├── User Story: Edit Profile (US-004)
    └── User Story: Upload Avatar (US-005)
```

**Implementation Trace**:
```javascript
// src/user/ (EPIC-001)
├── auth/ (FEAT-001)
│   ├── login.js (US-001)
│   ├── register.js (US-002)
│   └── password.js (US-003)
└── profile/ (FEAT-002)
    ├── edit.js (US-004)
    └── avatar.js (US-005)
```

## Pattern 5: Contract Testing Trace

**Description**: Trace API contracts to integration tests

**Structure**:
```
API Contract → Integration Tests → Contract Tests
```

**Example**:

### OpenAPI Contract
```yaml
# openapi.yaml
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
```

### Contract Tests
```javascript
// tests/contract/user-api.test.js
describe('User API Contract', () => {
  test('GET /users/{id} matches contract', async () => {
    const response = await request(app)
      .get('/users/123');

    expect(response.status).toBe(200);
    expect(response.headers['content-type']).toMatch(/json/);
    expect(response.body).toMatchSchema(userSchema);
  });

  test('Handles 404 for non-existent user', async () => {
    const response = await request(app)
      .get('/users/nonexistent');

    expect(response.status).toBe(404);
  });
});
```

## Traceability Commands

### View Traceability Chain
```bash
# View full trace for requirement
vic trace --requirement US-001

# View component trace
vic trace --component user-management

# View test coverage
vic trace --tests
```

### Validate Traceability
```bash
# Check all traces
vic trace validate

# Check missing traces
vic trace missing

# Check orphaned code
vic trace orphaned
```

### Generate Trace Report
```bash
# Generate HTML report
vic trace report --output traceability.html

# Generate JSON report
vic trace report --output traceability.json --format json
```

## Best Practices

### 1. Maintain Consistent Naming
```
US-001 → SPEC-REQ-001 → Feature-01 → test-01.js
```

### 2. Update Traces When Changing Code
- When implementing, add test references
- When refactoring, update traces
- When deleting, clean up traces

### 3. Use Traceability Early
- Start tracing during requirements phase
- Implement traces incrementally
- Review traces regularly

### 4. Automate Trace Checks
- Include in CI/CD pipeline
- Run trace validation on commits
- Report trace gaps regularly

### 5. Visualize Traces
```bash
# Generate graph
vic trace graph --output trace-graph.dot
dot -Tpng trace-graph.dot -o trace-graph.png
```

## Common Issues

### 1. Broken Traces
**Problem**: Implementation doesn't match requirements

**Solution**:
- Use `vic trace validate` to find issues
- Update implementation or requirements
- Document deviations

### 2. Missing Tests
**Problem**: No tests for implemented features

**Solution**:
- Add test files with proper naming
- Use TDD approach
- Mock external dependencies

### 3. Orphaned Code
**Problem**: Code without requirements or tests

**Solution**:
- Review for potential requirements
- Create tests if valid
- Delete if truly unused

### 4. Circular Dependencies
**Problem**: Requirements depend on each other circularly

**Solution**:
- Break into smaller requirements
- Use dependency injection
- Document intentional dependencies

## Advanced Patterns

### Event-Driven Traceability
```javascript
// Event-based tracing
eventEmitter.on('user:created', (user) => {
  trace('US-004', 'user-service', 'create-user', user.id);
});
```

### Database Traceability
```sql
-- Add trace metadata to database
ALTER TABLE users ADD COLUMN trace_id VARCHAR(50);
UPDATE users SET trace_id = 'US-001' WHERE id = 123;
```

### A/B Testing Traceability
```javascript
// Track different implementations
const implementation = getImplementationVariant();
if (implementation === 'new') {
  trace('US-001', 'new-implementation');
} else {
  trace('US-001', 'old-implementation');
}
```