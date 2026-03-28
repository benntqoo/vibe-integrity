# SPEC Templates

## Template 1: User Story Format

```markdown
### US-XXX: [Brief Description]
- As a [role], I want [feature], so that [value]
- Acceptance Criteria:
  - [Criteria 1]
  - [Criteria 2]
  - [Criteria 3]
```

## Template 2: Technical Specification

```markdown
# SPEC-[FEATURE].md

## Overview
[1-2 sentences describing the feature]

## Requirements
### Functional Requirements
- [Requirement 1]
- [Requirement 2]

### Non-Functional Requirements
- Performance: [Metrics]
- Security: [Requirements]
- Scalability: [Requirements]

## Architecture
### Component Diagram
```
[ASCII diagram or image reference]
```

### Data Flow
```
[Description of data flow]
```

## API Design
### Endpoints
- Method: Path → Description
- GET /api/resource → Get resource
- POST /api/resource → Create resource

### Request/Response Examples
```json
// Request
{
  "field": "value"
}

// Response
{
  "id": "123",
  "field": "value"
}
```

## Database Schema
```sql
CREATE TABLE table_name (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation Notes
- [Important considerations]
- [Edge cases to handle]
- [Integration points]
```

## Template 3: Architecture Decision Record (ADR)

```markdown
# ADR-[NUMBER]: [Decision Title]

## Status
[Accepted | Proved | Rejected]

## Context
[Description of the context and problem]

## Decision
[What was decided and why]

## Consequences
[Positive and negative consequences]
- Good: [Benefit 1]
- Good: [Benefit 2]
- Bad: [Drawback 1]
- Bad: [Drawback 2]
```

## Template 4: Test Plan

```markdown
# Test Plan for [Feature]

## Test Cases
### Test Case 1: [Scenario]
- Input: [Data]
- Expected Output: [Result]
- Actual Output: [Result]
- Status: [Pass/Fail]

### Test Case 2: [Edge Case]
- Input: [Data]
- Expected Output: [Result]
- Actual Output: [Result]
- Status: [Pass/Fail]

## Test Coverage
- Unit Tests: [X%]
- Integration Tests: [X%]
- E2E Tests: [X%]
```

## Template 5: SPEC Validation Check

```markdown
# SPEC Validation Report

## Gate 0: Requirements Completeness
### Check Items
- [✓] All user stories have acceptance criteria
- [✓] Requirements are testable
- [✓] No ambiguous language
- [✓] Priority levels defined

### Issues Found
- [ ] Issue description
- [ ] Issue description

## Gate 1: Architecture Completeness
### Check Items
- [✓] Technology stack selected
- [✓] Module boundaries defined
- [✓] API contracts designed
- [✓] Data schema defined

### Issues Found
- [ ] Issue description
```

## Template Usage Guide

1. **Choose the right template** based on your needs
2. **Fill in placeholders** with specific information
3. **Customize** as needed for your project
4. **Maintain consistency** across SPECs
5. **Use version control** to track changes