---
name: spec-workflow
description: Handles requirements analysis, architecture design, and SPEC creation.
metadata:
  domain: product
  version: "1.0"
  tags: [requirements, architecture, spec, design, user-stories]
  examples:
    - "User requirements are ambiguous"
    - "Need to design system architecture"
    - "Freeze requirements into SPEC"
  priority: critical
  auto_activate: false
---

# SPEC Workflow

## Overview

Handles the complete workflow from vague requirements to frozen SPEC. Combines requirements analysis, architecture design, UI/UX design, and SPEC creation.

**Merged from:** requirements + architecture + design-review + spec-architect

## L1: When to Use

| Situation | Use Skill? |
|-----------|------------|
| Requirements are vague or ambiguous | ✅ Yes |
| Need to design system architecture | ✅ Yes |
| Create or update SPEC documents | ✅ Yes |
| UI/UX design decisions | ✅ Yes |
| Simple code changes (no spec needed) | ❌ No |
| Debugging existing code | ❌ No |

## L1: Auto-Activate Triggers

| Trigger | When |
|---------|------|
| User explicitly invokes | User asks for requirements clarification |
| `spec-workflow` mentioned | User mentions SPEC, architecture, design |
| Requirements vague | User describes vague requirements |
| Architecture needed | User asks to design system |
| SPEC creation | User asks to create or update SPEC |

## L2: How to Use

### Phase 1: Requirements Analysis

1. **Clarify Requirements**
   - Identify vague parts
   - Ask clarifying questions
   - Define acceptance criteria

2. **Create User Stories**
   - Format: "As a [role], I want [feature], so that [value]"
   - Include priority (P0/P1/P2)
   - Define acceptance criteria

### Phase 2: Architecture Design

3. **Design System Architecture**
   - Select technology stack
   - Define module structure
   - Design API contracts
   - Consider scalability

### Phase 3: SPEC Creation

4. **Create SPEC Documents**
   - SPEC-REQUIREMENTS.md (user stories, acceptance criteria)
   - SPEC-ARCHITECTURE.md (design, tech stack, modules)

5. **Validate SPEC**
   - Run `vic spec gate 0` (requirements completeness)
   - Run `vic spec gate 1` (architecture completeness)
   - Fix any issues

## L3: References (Required Reading)

These references are part of the skill, not optional:

### Required (Always Read)
- `references/spec-workflow-guide.md` - Complete usage guide

### Optional (Read if Needed)
- `references/examples.md` - More examples
- `references/templates.md` - SPEC templates
