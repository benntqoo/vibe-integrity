# Implementation Guide

## Overview

This guide covers the complete implementation lifecycle from coding to testing to SPEC alignment.

## Option A: Feature Implementation (TDD)

### RED Phase
1. Write failing test
2. Run test to confirm failure
3. Write minimal code to pass

### GREEN Phase
1. Write minimal implementation
2. Run tests to confirm pass
3. Do not refactor yet

### REFACTOR Phase
1. Improve code structure
2. Run tests to confirm still pass
3. Repeat until satisfied

## Option B: Bug Fix (Systematic Debugging)

### 1. SURVEY
- Gather evidence
- Identify symptoms
- Document environment

### 2. PATTERN
- Find similar issues
- Check known patterns
- Research solutions

### 3. HYPOTHESIS
- Form testable hypothesis
- Design experiment
- Test hypothesis

### 4. IMPLEMENT
- Fix root cause
- Verify fix
- Add regression test

## Option C: SPEC Alignment Check

### When to Run
- After any code change
- Before committing
- During code review

### How to Run
```bash
vic spec gate 2
```

### If Fails
1. Read drift report
2. Option A: Update SPEC (preferred)
3. Option B: Fix code alignment

## Test Coverage

### Minimum Coverage
- Unit tests for business logic
- Integration tests for APIs
- E2E tests for critical paths

### Coverage Targets
| Type | Target |
|------|--------|
| Unit | 80%+ |
| Integration | 60%+ |
| E2E | 40%+ |
