---
name: vibe-redesign
description: Use when user presents a feature request to explore what the "10-star product" really is before implementation.
---

# Vibe Redesign - Product Discovery

## Overview

**Do NOT implement the literal request.** First ask: "What is this product actually for?"

This skill implements the "Brian Chesky mode" - rethinking the problem from the user's perspective to find the version that feels inevitable, delightful, and maybe even a little magical.

## When to Use

Activate when user presents ANY feature request. Do NOT skip this step even for "simple" requests.

## The Four Modes

### 1. EXPANSION - Scope Expansion

Dream big. The AI proposes the ambitious version. Every expansion is presented as an individual decision the user opts into.

**Activation:** When user wants to explore possibilities

**Example:**
User: "Let sellers upload a photo for their item."

AI Response:
```
If the real product is "help sellers create listings that actually sell",
the whole plan changes:

🎯 FEATURE: Smart Listing Creation

Instead of just "photo upload", consider:

1. 📸 Photo Intelligence
   - Auto-identify product from photo
   - Detect SKU/model number
   - Suggest best hero image
   - Flag low-quality/ugly photos

2. 📝 Content Generation
   - Draft title and description automatically
   - Pull specs and pricing comps from web
   - SEO optimization

3. ✨ Premium Experience
   - Remove background automatically
   - Add professional lighting
   - Make it feel premium, not like a 2007 form

Each is a separate decision. Which would you like to pursue?
```

### 2. SELECTIVE - Selective Expansion

Hold current scope as baseline, but surface what else is possible. Present opportunities one by one with neutral recommendations.

**Activation:** When user wants to evaluate trade-offs

**Output Format:**
```
📋 Current Scope: [User's original request]

🔍 Opportunities:

1. [Feature Name]
   - What: [Brief description]
   - Effort: Low / Medium / High
   - Impact: Low / Medium / High
   - Recommendation: [Why you might want it]

2. [Feature Name]
   - What: [Brief description]
   - ...

Your choice: [Which opportunities to pursue]
```

### 3. HOLD - Hold Scope

Maximum rigor on the existing plan. No expansions surfaced.

**Activation:** When user explicitly wants to stay focused, or time is constrained

**Process:**
1. Validate the current request is correctly understood
2. Identify any ambiguities or edge cases
3. Lock down the scope
4. Proceed to implementation planning

### 4. REDUCTION - Scope Reduction

Find the minimum viable version. Cut everything else.

**Activation:** When user wants to ship fast

**Process:**
1. Identify the ONE core value proposition
2. Remove all nice-to-haves
3. Define MVP scope clearly
4. Suggest a path for future expansion

## Workflow

### Step 1: Understand the Request

```
Ask: "Can you tell me more about what you're trying to achieve?"

Then reflect back:
"From what I understand, you want [interpretation]. 
Is that right? What's the core problem you're solving?"
```

### Step 2: Explore the "Why"

```
Ask: "What would success look like? What would the user 
feel when this feature works perfectly?"
```

### Step 3: Apply the Mode

Based on context and user preference, apply the appropriate mode.

### Step 4: Document the Decision

Create `docs/PRODUCT-REDESIGN.md`:

```markdown
# Product Redesign: [Feature Name]

## Original Request
[User's literal request]

## Real Product
[What the product is actually for]

## Selected Mode
[EXPANSION / SELECTIVE / HOLD / REDUCTION]

## Decisions Made

| Decision | Description | Effort | Impact |
|----------|-------------|--------|--------|
| D-001 | [Decision] | Medium | High |
| D-002 | [Decision] | Low | Medium |

## Next Steps

- [ ] Proceed to SPEC-REQUIREMENTS.md with this scope
- [ ] Or continue exploring specific decisions
```

## Integration with VIC-SDD

After redesign is complete:

1. Update `.vic-sdd/tech/tech-records.yaml` with product decisions:
   ```yaml
   decisions:
     - id: PROD-001
       type: product-redesign
       trigger: "[Original request]"
       real_product: "[What we decided]"
       mode: "[Selected mode]"
   ```

2. Proceed to `vibe-think` for requirements clarification

3. Create/update `SPEC-REQUIREMENTS.md` with validated scope

## Common Traps

### Trap 1: Implementing Literally
❌ "User said photo upload, so I'll add a file picker"

✅ "User wants sellers to create sellable listings"

### Trap 2: Missing the 10x
❌ "User wants email notifications, I'll add email support"

✅ "User wants to stay informed without checking constantly"

### Trap 3: Scope Creep
❌ "This is a great idea, let's add everything"

✅ "Here's what's possible. Which do you want?"

## Quick Reference

| User Need | Recommended Mode |
|-----------|------------------|
| Explore possibilities | EXPANSION |
| Evaluate trade-offs | SELECTIVE |
| Stay focused | HOLD |
| Ship fast | REDUCTION |

## Invocation

```bash
# Activate this skill
skill vibe-redesign

# Or when starting a new feature
"Help me redesign [feature request]"
```

---

## Pipeline Metadata

pipeline_metadata:
  handoff:
    delivers:
      - artifact: "docs/PRODUCT-REDESIGN.md"
        description: "Product redesign decision with selected mode (EXPANSION/SELECTIVE/HOLD/REDUCTION)"
      - artifact: ".vic-sdd/tech/tech-records.yaml"
        description: "Product decisions recorded (via vic rt)"
    consumes:
      - artifact: "user's feature request"
        description: "Original request to explore"
      - artifact: "SPEC-REQUIREMENTS.md (draft)"
        description: "Existing requirements context"
  exit_condition:
    success: "Product scope validated, mode selected, decisions recorded"
    failure: "No clear product vision — use HOLD mode, stay focused"
    triggers_next_on_success: "vibe-think (clarify selected scope)"
    triggers_next_on_failure: "vibe-think (proceed with HOLD mode)"
  agent_pattern: Generator
