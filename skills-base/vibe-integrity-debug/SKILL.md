---
name: vibe-integrity-debug
description: Systematic debugging helper for Vibe Integrity that ensures root cause analysis before fixes, integrating with project architecture memory
---

# Vibe Integrity Debug

## Overview

Vibe Integrity Debug is a systematic debugging helper designed specifically for use with the Vibe Integrity framework. It ensures that before attempting any fixes, you thoroughly investigate the root cause of issues, preventing the common pitfall of treating symptoms rather than underlying problems.

This skill adapts the principles of systematic debugging to work within the Vibe Integrity ecosystem, ensuring that debugging activities are properly recorded in the project's architecture memory (.vibe-integrity/) when they reveal insights about system design, risks, or technical decisions.

## Core Philosophy

**Never fix a symptom without understanding the root cause.** Vibe Integrity Debug enforces a four-phase process that must be completed in order:

1. **Root Cause Investigation** - Understand what and why the issue occurs
2. **Pattern Analysis** - Compare against working examples and references  
3. **Hypothesis and Testing** - Form and test a single, specific hypothesis
4. **Implementation** - Fix the root cause, not the symptom

Each phase builds on the previous one, and you cannot proceed to the next phase without completing the current one.

## When to Use

Use Vibe Integrity Debug for ANY technical issue within a Vibe Integrity-managed project:
- Test failures
- Bugs in functionality
- Unexpected behavior
- Performance problems
- Build or type-check failures
- Integration issues
- Vibe Guard validation failures

**Use this ESPECIALLY when:**
- Under time pressure (when guessing is most tempting)
- A "quick fix" seems obvious
- You've already tried fixes that didn't work
- Previous fixes introduced new problems
- You don't fully understand why the issue occurs
- The issue relates to architecture, dependencies, or project structure

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix, you MUST:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings - they often contain the exact solution
   - Read stack traces completely, noting line numbers, file paths, error codes
   - Check Vibe Guard reports if relevant (validate-vibe-guard.py output)

2. **Reproduce Consistently**
   - Can you trigger the issue reliably?
   - What are the exact steps to reproduce?
   - Does it happen every time under the same conditions?
   - If not reproducible → gather more diagnostic data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this? (git diff, recent commits)
   - New dependencies, configuration changes, environmental differences
   - Check .vibe-integrity/ files for recent architectural decisions that might be related

4. **Gather Evidence in Multi-Component Systems**
   When your system has multiple components (frontend → backend → database, etc.):
   
   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters the component
     - Log what data exits the component  
     - Verify environment/config propagation
     - Check state at each layer
   ```
   
   Run this to gather evidence showing WHERE the issue breaks
   THEN analyze to identify the failing component
   THEN investigate that specific component

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in the same codebase
   - What works that's similar to what's broken?
   - Check module-map.yaml and dependency-graph.yaml for related components

2. **Compare Against References**
   - If implementing a known pattern, read the reference implementation completely
   - Don't skim - understand every line before applying
   - Check tech-records.yaml for past decisions about similar patterns

3. **Identify Differences**
   - What's different between working and broken implementations?
   - List every difference, however small
   - Don't assume "that can't matter" - small differences often root causes

4. **Understand Dependencies**
   - What other components, services, or configurations does this need?
   - What assumptions does the code make about its environment?
   - Check risk-zones.yaml for known issues in related areas

### Phase 3: Hypothesis and Testing

**Follow the scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think [X] is the root cause because [Y]"
   - Write it down before testing
   - Be specific and falsifiable, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test your hypothesis
   - Change only one variable at a time
   - Never fix multiple things in one go

3. **Verify Before Continuing**
   - Did your test confirm the hypothesis? → Proceed to Phase 4
   - Did it fail? → Form a NEW hypothesis based on new information
   - NEVER add more fixes on top of a failed hypothesis

4. **When You Truly Don't Know**
   - Say "I don't understand [X]" - this is professional, not weak
   - Ask for help or research more before guessing
   - Consider if this might indicate an architectural misunderstanding

### Phase 4: Implementation

**Fix only what you've proven to be the root cause:**

1. **Create Failing Test Case**
   - Build the simplest possible reproduction of the issue
   - Prefer automated tests, but a test script is acceptable
   - You MUST have this BEFORE attempting any fix
   - Consider using superpowers:test-driven-development for proper test creation

2. **Implement Single Fix**
   - Address ONLY the root cause you identified and verified
   - Make exactly one change at a time
   - No "while I'm here" improvements or refactoring
   - No bundled changes - isolate the fix to the proven cause

3. **Verify the Fix**
   - Does your test case now pass?
   - Have you verified no other tests or functionality broke?
   - Is the original issue actually resolved in all contexts?

4. **If the Fix Doesn't Work**
   - STOP immediately
   - Ask: "How many fixes have I tried for this issue?"
   - If < 3: Return to Phase 1 with your new information
   - If ≥ 3: This strongly suggests an architectural issue - proceed to step 5

5. **If 3+ Fixes Failed: Question the Architecture**
   
   This is not personal failure - it's a signal that your mental model may be wrong.
   
   **Pattern indicating architectural problems:**
   - Each fix reveals new problems in different places
   - Fixes require "massive refactoring" to implement cleanly  
   - Each fix creates new symptoms elsewhere in the system
   
   **STOP and question fundamentals with your partner:**
   - Is this pattern/approach fundamentally sound for our project?
   - Are we continuing with it through inertia rather than effectiveness?
   - Should we consider refactoring the architecture instead of fixing symptoms?
   
   **Discuss this BEFORE attempting any more fixes**
   - Record insights in tech-records.yaml if you decide to change approach
   - Update risk-zones.yaml if you uncover new architectural risks

## Integration with Vibe Integrity

Vibe Integrity Debug enhances the Vibe Integrity framework by:

### Automatic Architecture Memory Updates
When debugging reveals insights about the system, consider updating:
- **tech-records.yaml**: New understanding of why components work as they do
- **risk-zones.yaml**: Discovery of hidden risks or confirmation of existing ones  
- **schema-evolution.yaml**: If debugging reveals data model misunderstandings
- **dependency-graph.yaml**: If you uncover incorrect assumptions about module relationships

### Workflow Integration
1. **Before debugging**: Check .vibe-integrity/ files for relevant context
2. **During debugging**: Consider what you're learning about the system
3. **After resolving**: Update relevant .vibe-integrity/ files with new insights
4. **Always**: Run validate-vibe-integrity.py to ensure structural integrity

## Red Flags - When to STOP and Return to Phase 1

If you catch yourself thinking or doing any of these, **STOP IMMEDIATELY** and return to Root Cause Investigation:

- "Quick fix for now, I'll investigate later"
- "Just try changing [X] and see if it works"  
- "Let me add multiple changes and run tests"
- "I'll skip the test - I'll manually verify it works"
- "It's probably [X], let me fix that first"
- "I don't fully understand [X] but this approach might work"
- "The pattern says [X] but I'll adapt it differently for our case"
- Listing fixes without having investigated root causes
- Proposing solutions before completing evidence gathering
- "One more fix attempt" (when you've already tried 2+ fixes)
- Each fix attempt reveals a new problem in a different area

**ALL of these indicate: You're guessing, not debugging. Return to Phase 1.**

## Your Partner's Signals You're Off Track

Watch for these indications from your collaborator that you've skipped the process:

- "Is that actually happening?" - You assumed without verification
- "How do we know [Y] is true?" - You should have gathered evidence first  
- "Let's stop guessing" - You're proposing fixes without understanding
- "We need to understand the fundamentals here" - You're treating symptoms
- "Are we stuck in a loop?" - Frustration from cycling through failed fixes

**When you observe these: STOP. Return to Phase 1 immediately.**

## Special Considerations for Vibe Integrity Projects

When debugging in a Vibe Integrity-managed project:

### Context from Architecture Memory
Before starting investigation, review:
- **project.yaml**: Current tech stack and project status
- **tech-records.yaml**: Past decisions that might relate to the issue
- **risk-zones.yaml**: Known problem areas to consider
- **dependency-graph.yaml**: Module relationships that might be involved
- **schema-evolution.yaml**: Recent data model changes

### When Debugging Reveals Architectural Insights
If your debugging work leads to new understanding about:
- Why certain architectural decisions were made
- Hidden risks in current approaches  
- Better ways to structure related components
- Data flow or integration misunderstandings

**Consider recording these insights** in the appropriate .vibe-integrity/ files to strengthen the project's architecture memory for future AI sessions.

## Summary: The Vibe Integrity Debug Mantra

> **"No fixes without root cause evidence.  
> One hypothesis at a time.  
> Verify before proceeding.  
> If three attempts fail, question the architecture."**

By following this process consistently, you'll:
- Fix issues faster in the long run (despite short-term perception)
- Introduce far fewer new bugs
- Develop deeper understanding of your Vibe Integrity-managed system
- Contribute meaningful insights to the project's architecture memory
- Build trust in your debugging process with teammates