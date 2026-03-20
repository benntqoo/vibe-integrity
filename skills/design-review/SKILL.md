# Design Review Skill

## Overview

Combines vibe-design for design system consultation and review.

**When to use:**
- Project has no design system
- Reviewing existing UI for AI slop patterns

## Mode 1: Design System Building

### Process

1. **Understand the product**
   - What does your product do?
   - Who are your users?
   - What feeling should it convey?

2. **Research the landscape**
   - Take screenshots of real sites in your space
   - Analyze fonts, colors, spacing

3. **Define Design System**

```markdown
# Design System: [Project]

## Aesthetic Direction
[Industrial/Utilitarian | Playful | Premium | Minimal]

## Typography
- Display: [Font Name] - Headings
- Body: [Font Name] - Paragraphs
- Mono: [Font Name] - Code

## Color Palette
- Primary: #XXXXXX
- Secondary: #XXXXXX
- Accent: #XXXXXX
- Background: #XXXXXX
- Text: #XXXXXX

## Spacing Scale
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px
```

## Mode 2: Design Review (80-Item Audit)

### AI Slop Detection

| Pattern | AI Slop | Alternative |
|---------|---------|-------------|
| Hero | Gradient background | Bold typography |
| Layout | Three-column grid | Asymmetric layout |
| Radius | Uniform 8px | Varied by element role |

### Scoring

| Score | Meaning |
|-------|---------|
| 9-10 | Excellent - no AI patterns |
| 7-8 | Minor issues - polish pass |
| 5-6 | Some issues - targeted fixes |
| 3-4 | Major issues - significant work |
| 0-2 | Severe - rework needed |

## Output

Create `DESIGN.md` with full design system.

## When NOT to Use

- CLI tools without UI
- Backend-only projects
- Pure API services
