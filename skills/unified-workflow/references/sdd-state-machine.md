# SDD State Machine

## State Overview

The SDD (Software Delivery Decision) state machine manages the complete feature delivery lifecycle through 7 phases:

```
Ideation → Explore → SpecCheckpoint → Build → Verify → ReleaseReady → Released
```

## State Descriptions

### 1. Ideation
**Purpose**: Initial concept and requirement gathering
**Activities**:
- Gather user requirements
- Identify stakeholders
- Define scope
- Assess feasibility
- Create initial user stories

**Gate Check 0**: Requirements Completeness
- All user stories defined
- Acceptance criteria specified
- Requirements are testable
- Priority levels assigned

**Exit Conditions**:
- Requirements clearly defined
- Stakeholder alignment
- Scope boundaries set

### 2. Explore
**Purpose**: Research and design exploration
**Activities**:
- Technical research
- Architecture exploration
- Technology selection
- Risk assessment
- Prototype development (if needed)

**Gate Check 1**: Architecture Completeness
- Technology stack selected
- Module boundaries defined
- API contracts designed
- Data schema defined
- Scalability considerations addressed

**Exit Conditions**:
- Architecture decisions finalized
- Technical risks identified
- Prototype validated

### 3. SpecCheckpoint
**Purpose**: Freeze requirements and architecture
**Activities**:
- Create SPEC documents
- Review with stakeholders
- Get sign-off
- Finalize technical decisions

**Gate Check**: SPEC Validation
- SPEC-REQUIREMENTS.md complete
- SPEC-ARCHITECTURE.md complete
- All stakeholders reviewed
- Changes documented

**Exit Conditions**:
- SPEC documents frozen
- Stakeholder sign-off
- No major pending decisions

### 4. Build
**Purpose**: Implementation phase
**Activities**:
- Write code (TDD)
- Implement features
- Write tests
- Code review
- Integration

**Gate Check 2**: Code Alignment
- Code implements SPEC
- Code follows standards
- Tests pass
- Documentation updated

**Exit Conditions**:
- Feature implemented
- Tests passing
- Code reviewed

### 5. Verify
**Purpose**: Quality assurance
**Activities**:
- Run comprehensive tests
- Performance testing
- Security testing
- User acceptance testing
- Bug fixes

**Gate Check 3**: Test Coverage
- Unit tests complete
- Integration tests complete
- E2E tests complete
- Performance benchmarks met
- Security checks passed

**Exit Conditions**:
- All tests passing
- Quality metrics met
- No critical bugs

### 6. ReleaseReady
**Purpose**: Preparation for release
**Activities**:
- Final validation
- Release documentation
- Deployment planning
- Rollback strategy
- Communication plan

**Gate Check**: Release Readiness
- All previous gates passed
- Documentation complete
- Deployment plan ready
- Rollback strategy defined
- Stakeholders notified

**Exit Conditions**:
- Release-ready artifacts prepared
- Deployment plan approved
- All checks passed

### 7. Released
**Purpose**: Feature is live
**Activities**:
- Deploy to production
- Monitor performance
- Gather feedback
- Address issues
- Plan for next iteration

**Exit Conditions**:
- Feature deployed successfully
- Monitoring active
- Feedback collection ongoing

## State Transitions

### Automatic Transitions
- **Ideation → Explore**: After Gate 0 passes
- **Explore → SpecCheckpoint**: After Gate 1 passes
- **SpecCheckpoint → Build**: After SPEC sign-off
- **Build → Verify**: After Gate 2 passes
- **Verify → ReleaseReady**: After Gate 3 passes
- **ReleaseReady → Released**: After deployment

### Manual Transitions
```bash
# Force advance to specific phase
vic phase advance --to 3  # Force to Build

# Skip gates (use with caution)
vic phase advance --to 4 --skip-gates
```

## State Commands

### Check Current State
```bash
vic status
```

### Advance State
```bash
# Advance one phase
vic phase advance

# Advance to specific phase
vic phase advance --to 5
```

### View State History
```bash
vic phase history
```

### Pause State Changes
```bash
vic phase pause
```

### Resume State Changes
```bash
vic phase resume
```

## Gate Operations

### Run Gate Checks
```bash
# Check all gates
vic gate check

# Check only blocking issues
vic gate check --blocking

# Run specific gate
vic spec gate 2
```

### View Gate Status
```bash
vic gate status
```

### Fix Gate Issues
```bash
# View detailed issues
vic gate issues

# Auto-fix common issues
vic gate fix --auto
```

## State Management Best Practices

1. **Don't skip gates**: Each gate ensures quality
2. **Document decisions**: Why you advanced phases
3. **Review before advancing**: Stakeholder sign-off
4. **Monitor continuously**: Track metrics in each phase
5. **Be ready to rollback**: If issues arise

## Common Issues and Solutions

### Gate Failures
- **Problem**: Gate fails but need to proceed
- **Solution**: Document why it's safe to proceed
- **Command**: `vic gate override --reason "documentation"`

### State Stuck
- **Problem**: State won't advance
- **Solution**: Check for blockers, run gate check
- **Command**: `vic gate check --blocking`

### Performance Issues
- **Problem**: Phase taking too long
- **Solution**: Break into smaller tasks
- **Command**: `vic auto start --parallel`

### Resource Constraints
- **Problem**: Limited resources
- **Solution**: Prioritize, scope down
- **Command**: `vic phase scope --adjust`