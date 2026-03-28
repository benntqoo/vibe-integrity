# SPEC Workflow Examples

## Example 1: Requirements Clarification

**Scenario**: User provides vague requirements

**Input**:
> "I want a user management system"

**Steps**:
1. Identify vague parts
2. Ask clarifying questions
3. Define acceptance criteria

**Output**:
```yaml
User Stories:
  - As an admin, I want to create user accounts, so that users can access the system
  - As a user, I want to reset my password, so that I can recover access
  - As an admin, I want to deactivate users, so that I can manage access

Acceptance Criteria:
  - Users can register with email and password
  - Admin can view, create, edit, and deactivate users
  - Password reset via email
  - Role-based access control
```

## Example 2: Architecture Design

**Scenario**: Design microservices architecture

**Steps**:
1. Select technology stack
2. Define module structure
3. Design API contracts

**Output**:
```
Technology Stack:
  - Backend: Node.js + Express
  - Database: PostgreSQL
  - Cache: Redis
  - Message Queue: RabbitMQ

Module Structure:
  - auth-service: Authentication & authorization
  - user-service: User management
  - notification-service: Email & notifications
  - api-gateway: Request routing

API Contracts:
  POST /api/auth/login
  POST /api/auth/logout
  GET /api/users
  POST /api/users
  PUT /api/users/:id
```

## Example 3: SPEC Creation

**Scenario**: Freeze requirements into SPEC

**Files Created**:
- SPEC-REQUIREMENTS.md
- SPEC-ARCHITECTURE.md

**SPEC-REQUIREMENTS.md Content**:
```markdown
# SPEC-REQUIREMENTS.md

## User Stories

### US-001: User Registration
- As a new user, I want to register an account
- Acceptance Criteria:
  - Email validation
  - Password strength requirements
  - Duplicate email check

### US-002: User Login
- As a registered user, I want to login
- Acceptance Criteria:
  - Secure authentication
  - Session management
  - Failed login attempts tracking
```

**SPEC-ARCHITECTURE.md Content**:
```markdown
# SPEC-ARCHITECTURE.md

## System Architecture

### Component Overview
- Auth Service: Handles authentication
- User Service: Manages user data
- API Gateway: Routes requests

### Database Schema
```sql
Users:
  - id (PK)
  - email (unique)
  - password_hash
  - created_at
  - updated_at
  - status
```
```

## Example 4: SPEC Validation

**Scenario**: Validate SPEC completeness

**Commands**:
```bash
# Check requirements completeness
vic spec gate 0

# Check architecture completeness
vic spec gate 1
```

**Output Interpretation**:
- Gate 0 Passed: All requirements are clear and testable
- Gate 1 Passed: Architecture is complete and implementable
- Failures: Fix issues and re-run gates

## Example 5: SPEC Updates

**Scenario**: Update SPEC based on feedback

**Process**:
1. Review feedback
2. Update relevant sections
3. Re-run validation gates

**Example Update**:
```markdown
# Before
Password requirements: 8 characters

# After
Password requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character
```