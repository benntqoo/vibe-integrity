# Unified Workflow Examples

## Example 1: Complete Feature Delivery

**Scenario**: Implement a new user profile feature

### Phase 1: Start Delivery
```bash
vic auto start
```

**Output**:
```
✓ Project state loaded
✓ SPEC documents found
✓ Constitution rules validated
✓ Starting autonomous mode
Current phase: Ideation
```

### Phase 2: Requirements Analysis
Using spec-workflow skill to:
- Clarify requirements
- Create user stories
- Design architecture

### Phase 3: Advance to SpecCheckpoint
```bash
vic phase advance --to 2
```

**Output**:
```
✓ Running Gate 0: Requirements completeness
✓ All requirements clear and testable
✓ Phase advanced: Explore
```

### Phase 4: Architecture Design
Using spec-workflow skill to:
- Select tech stack
- Define modules
- Design APIs

### Phase 5: Advance to Build
```bash
vic phase advance --to 3
```

**Output**:
```
✓ Running Gate 1: Architecture completeness
✓ Architecture complete and implementable
✓ Phase advanced: Build
```

### Phase 6: Implementation
Using implementation skill to:
- Write code (TDD)
- Run tests
- Check alignment

### Phase 7: Advance to Verify
```bash
vic phase advance --to 4
```

**Output**:
```
✓ Running Gate 2: Code alignment
✓ Running Gate 3: Test coverage
✓ All gates passed
✓ Phase advanced: Verify
```

### Phase 8: Pre-Commit Check
```bash
vic gate check --blocking
```

**Output**:
```
✓ Constitution rules satisfied
✓ No blocking issues found
✓ SPEC hash unchanged
✓ Ready for commit
```

### Phase 9: End Delivery
```bash
vic auto stop
```

**Output**:
```
✓ Delivery completed successfully
✓ Traceability verified
✓ Backup saved to: .vic-sdd/backup-2024-03-26.json
```

## Example 2: Pre-Commit Validation

**Scenario**: Check before committing changes

### Run Constitution Check
```bash
vic constitution check
```

**Output**:
```
Constitution Check Results:
=========================
✓ Single Responsibility Principle: PASSED
✓ Don't Repeat Yourself: PASSED
✓ Open/Closed Principle: PASSED
✓ Dependency Inversion: PASSED
✓ SOLID Principles: PASSED
```

### Run Gate Checks
```bash
vic gate check --blocking
```

**Output**:
```
Gate Check Results:
==================
✓ Gate 0: Requirements completeness - PASSED
✓ Gate 1: Architecture completeness - PASSED
✓ Gate 2: Code alignment - PASSED
✓ Gate 3: Test coverage - PASSED
✓ No blocking issues
```

### SPEC Hash Check
```bash
vic spec hash
```

**Output**:
```
SPEC Hash: abc123def456
Status: Unchanged since last session
```

### Cost Status
```bash
vic cost status
```

**Output**:
```
Session Cost:
============
Tokens used: 45,678
Budget remaining: 154,322
Status: Within budget
```

## Example 3: Traceability Verification

**Scenario**: Verify requirements-to-code mapping

### View Traceability Chain
```bash
vic history --limit 10
```

**Output**:
```
Traceability Chain:
===================
US-001 → SPEC-REQ-001 → src/auth/login.js → tests/auth.test.js
US-002 → SPEC-REQ-002 → src/user/profile.js → tests/user.test.js
US-003 → SPEC-REQ-003 → src/notification/email.js → tests/notification.test.js
```

### Check Specific Requirement
```bash
vic trace --requirement US-001
```

**Output**:
```
Requirement US-001: User Registration
=====================================
✓ User story defined
✓ SPEC-REQ-001 created
✓ Implementation: src/auth/register.js
✓ Tests: tests/auth.register.test.js
✓ Status: Complete
```

## Example 4: Phase Management

**Scenario**: Manually manage SDD phases

### Check Current Phase
```bash
vic status
```

**Output**:
```
Current Phase: Build
===================
- Started: 2024-03-26 10:00
- Next Phase: Verify
- Gates to run: Gate 2 (Code alignment)
```

### Advance to Next Phase
```bash
vic phase advance
```

**Output**:
```
Advancing to Verify phase
========================
✓ Running Gate 2: Code alignment
✓ Code aligns with SPEC
✓ Phase advanced: Verify
```

### Force Phase Change
```bash
vic phase advance --to 5
```

**Output**:
```
Forcing phase to ReleaseReady
===========================
⚠️  Skipping Gates 3 and 4
⚠️  Manual verification required
⚠️  Use with caution
```

## Example 5: Autonomous Mode Operations

**Scenario**: Use autonomous mode for repetitive tasks

### Start Autonomous Session
```bash
vic auto start --mode batch
```

**Output**:
```
Starting autonomous mode in batch mode
=====================================
✓ Loading configuration
✓ Checking dependencies
✓ Starting work queue
✓ Monitoring progress
```

### Monitor Progress
```bash
vic auto status
```

**Output**:
```
Autonomous Mode Status:
========================
Status: Running
Tasks completed: 5/10
Tasks remaining: 5
Token usage: 23,456
Estimated completion: 15 minutes
```

### Pause and Resume
```bash
vic auto pause
```

```bash
vic auto resume
```

### Stop with Summary
```bash
vic auto stop --summary
```

**Output**:
```
Session Summary:
================
Duration: 2h 15m
Tasks completed: 8/10
Code files modified: 15
Tests added: 12
Issues found: 3 (fixed)
Token usage: 45,678
Recommendations for next session:
1. Improve test coverage for payment module
2. Add error handling for API calls
3. Update documentation
```