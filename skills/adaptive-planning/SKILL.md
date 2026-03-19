---
name: adaptive-planning
description: Use when research reveals discrepancies with original plan, or when user wants to reassess the roadmap after learning new information.
---

# Adaptive Planning - Reassessment Mode

## Overview

Plans are living documents. When new information is discovered, reassess and adapt.

This skill implements adaptive planning - the ability to re-evaluate and adjust plans based on:
- Research findings that contradict assumptions
- Technical discoveries (easier/harder than expected)
- User feedback
- Changing requirements
- External factors

## When to Use

Activate when:

1. **After each major milestone/slice completes** - Automatic trigger
2. **Research reveals discrepancy** - Findings contradict original assumptions
3. **Technical surprises** - Something is much easier/harder than expected
4. **User requests reassessment** - Explicit `vic replan` command
5. **Environment changes** - New tools, dependencies, or constraints

## The Reassessment Flow

### Step 1: Detect Trigger

Ask: "Does this finding change anything?"

```
Examples:
- "We found a library that does this in 10 lines"
- "The API doesn't support this use case"
- "Users responded negatively to this in testing"
- "The original assumption about scale was wrong"
```

### Step 2: Assess Impact

For each discrepancy, evaluate:

| Dimension | Questions |
|-----------|------------|
| **Scope** | Does this change what we build? |
| **Timeline** | Does this affect delivery date? |
| **Quality** | Does this affect product quality? |
| **Cost** | Does this change resource requirements? |

### Step 3: Generate Options

Present adaptation options:

```
📋 Impact Assessment: [Finding]

Options:

[1] ADAPT SCOPE
   Change: [What to modify]
   Reason: [Why this is better]
   Impact: [What else it affects]
   Decision: [Proceed?]

[2] ADAPT TIMELINE
   Change: [New estimate]
   Reason: [What caused the change]
   Impact: [Deliverable impact]
   Decision: [Accept new timeline?]

[3] ADAPT APPROACH
   Change: [New technical approach]
   Reason: [Why this is better]
   Impact: [What to reconsider]
   Decision: [Switch approach?]

[4] MAINTAIN COURSE
   Reason: [Why this doesn't change anything]
   Decision: [Continue as planned?]
```

### Step 4: Document Decision

Update `.vic-sdd/status/replan-log.yaml`:

```yaml
replan_history:
  - timestamp: "2026-03-19T10:30:00Z"
    trigger: research_discrepancy
    finding: "[What was discovered]"
    original_plan: "[What we assumed]"
    new_plan: "[What we decided]"
    reason: |
      [Why this change makes sense]
    user_approved: true
    impact:
      scope_changes: ["Change 1", "Change 2"]
      timeline_impact: "+2 hours"
      effort: medium
```

### Step 5: Update SPEC

If changes are approved:

1. Update `SPEC-ARCHITECTURE.md` if architecture changed
2. Update `SPEC-REQUIREMENTS.md` if requirements changed
3. Re-run Gate 1 (Architecture) if needed
4. Notify team of changes

## Trigger Scenarios

### Scenario 1: Research Complete

```
After: Research phase completes

Ask: "Did research reveal anything that changes our approach?"

If yes → Trigger reassessment
If no → Continue to planning
```

### Scenario 2: Slice Complete

```
After: Each slice completes

Ask: "Given what we learned, should we adjust remaining slices?"

Review:
- Original estimates vs actual
- Discovered dependencies
- New opportunities
- Risks that materialized
```

### Scenario 3: User Request

```
Command: vic replan

Process:
1. Show current plan
2. Ask what triggered replan
3. Assess impact
4. Generate options
5. Document decision
```

## Impact Analysis Template

```markdown
# Reassessment: [What Triggered This]

## Trigger
- Type: [research_complete / slice_complete / user_request / technical_surprise]
- Date: [When]
- Source: [Who/What]

## Current Plan
[What we planned]

## New Information
[What we discovered]

## Impact Analysis

| Aspect | Original | New | Delta |
|--------|----------|-----|-------|
| Scope | | | |
| Timeline | | | |
| Effort | | | |
| Quality | | | |

## Options Considered

### Option A: [Name]
- Change: [What]
- Pros: [Benefits]
- Cons: [Costs]
- Recommendation: [Yes/No]

### Option B: [Name]
- ...

## Decision

[What was decided]

## Approval
- [ ] User approved
- [ ] Recorded to replan-log.yaml
- [ ] SPEC updated (if applicable)
```

## Common Patterns

### Pattern 1: Scope Expansion
```
Finding: "There's a library that does 80% of this"

Options:
- Add library (saves time, adds dependency)
- Build from scratch (more control, more effort)

Decision: Usually add library, if dependency is acceptable
```

### Pattern 2: Scope Reduction
```
Finding: "This feature is much harder than expected"

Options:
- Cut feature
- Simplify feature
- Extend timeline

Decision: Usually simplify or cut
```

### Pattern 3: Approach Change
```
Finding: "Our architecture won't support this scale"

Options:
- Change architecture
- Add scaling layer
- Accept limitations

Decision: Depends on timeline and budget
```

### Pattern 4: False Assumption
```
Finding: "We assumed X, but X is wrong"

Options:
- Update assumption
- Investigate further
- Proceed with corrected assumption

Decision: Always update assumption first
```

## Integration with VIC-SDD

### Trigger Points

1. **vic spec gate 1** - After architecture review
2. **vic phase advance** - After phase completion
3. **vic replan** - Explicit user request

### Required Actions

1. **Record to replan-log.yaml**
2. **Update SPEC if needed**
3. **Re-run relevant Gate checks**
4. **Notify team of changes**

## Anti-Patterns

### Anti-Pattern 1: Paralysis
❌ "We found something new, let's stop everything and reassess everything"

✅ "This specific finding affects this specific part. Let's address it."

### Anti-Pattern 2: Ignoring Signals
❌ "That's interesting, but let's stick to the plan"

✅ "Let's evaluate this finding properly. Here's my assessment..."

### Anti-Pattern 3: Scope Creep
❌ "We discovered something, let's add it to scope"

✅ "We discovered something. Options: add to scope, backlog it, or note and proceed."

## Quick Reference

| Trigger | Action |
|---------|--------|
| Research complete | Ask: "Change anything?" |
| Slice complete | Review vs original plan |
| Technical surprise | Assess impact, generate options |
| User request | Run full reassessment flow |
| Environment change | Evaluate relevance, adapt if needed |

---

## Pipeline Metadata

pipeline_metadata:
  handoff:
    delivers:
      - artifact: ".vic-sdd/status/replan-log.yaml"
        description: "Replan history entry with trigger, finding, decision, impact"
      - artifact: "SPEC-REQUIREMENTS.md or SPEC-ARCHITECTURE.md (updated)"
        description: "Updated specs if scope or timeline changed"
    consumes:
      - artifact: "original plan"
        description: "What was originally planned"
      - artifact: "new information"
        description: "Research finding, technical surprise, or user feedback"
  exit_condition:
    success: "Plan reassessed, decision made, documented in replan-log.yaml"
    failure: "Cannot reach consensus on adaptation — maintain course"
    triggers_next_on_success: "continue with adjusted plan or maintain original plan"
    triggers_next_on_failure: "pre-decision-check (evaluate options)"
  agent_pattern: Reviewer
