# SPEC Workflow Guide

## Overview

This guide covers the complete SPEC Workflow for going from vague requirements to frozen SPEC.

## Phase 1: Requirements Analysis

### 1.1 Requirements Gathering

**Questions to Ask:**
- What is the user's goal?
- Who are the stakeholders?
- What constraints exist?
- What are the success criteria?

**Output:** Raw requirements list

### 1.2 Requirements Clarification

**Techniques:**
- 5 Whys (dig deeper)
- User stories format
- Acceptance criteria

**User Story Template:**
```
As a [role]
I want [feature]
So that [value]
```

### 1.3 Requirements Validation

**Checklist:**
- [ ] All stakeholders aligned
- [ ] Acceptance criteria defined
- [ ] Priority assigned
- [ ] Dependencies identified

## Phase 2: Architecture Design

### 2.1 Technology Selection

**Criteria:**
- Team expertise
- Scalability needs
- Integration requirements
- Performance targets
- Security requirements

### 2.2 System Architecture

**Deliverables:**
- Module structure
- API contracts
- Data models
- Deployment diagram

## Phase 3: SPEC Document Creation

### 3.1 SPEC-REQUIREMENTS.md

**Sections:**
- User stories
- Acceptance criteria
- Non-functional requirements
- Constraints

### 3.2 SPEC-ARCHITECTURE.md

**Sections:**
- Technology stack
- Module structure
- API design
- Data models
- Security considerations

## Common Mistakes

| Mistake | Prevention |
|---------|------------|
| Vague requirements | Use acceptance criteria |
| Skipping validation | Run Gate 0 |
| No priority | Use MoSCoW method |
| Missing constraints | Document upfront |
