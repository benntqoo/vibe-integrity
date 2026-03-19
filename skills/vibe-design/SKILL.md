---
name: vibe-design
description: Use when building design systems from scratch, reviewing designs, or auditing for AI-generated patterns.
---

# Vibe Design - Design System & AI Slop Detection

## Overview

Two modes: **Design System Building** and **Design Review with AI Slop Detection**.

## Mode 1: Design System Consultation

### When to Use

When project has no design system yet - no fonts, colors, or layout choices.

### Process

1. **Understand the product**
```
Ask: "What does your product do?"
Ask: "Who are your users?"
Ask: "What feeling should it convey?"
```

2. **Research the landscape**
```
Take screenshots of real sites in your space
Analyze fonts, colors, spacing
Understand conventions before breaking them
```

3. **Propose design system**

**Aesthetic Direction:**
- Define the overall feeling
- Examples: Industrial/Utilitarian, Playful, Premium, Minimal

**Typography:**
```
Display Font (headings): [Font Name] - Used for H1, H2
Body Font: [Font Name] - Used for paragraphs
Mono Font: [Font Name] - Used for code/data
```

**Color Palette:**
```
Primary: #XXXXXX - Main brand color
Secondary: #XXXXXX - Supporting color
Accent: #XXXXXX - Call-to-action color
Background: #XXXXXX / #XXXXXX (light/dark)
Text: #XXXXXX / #XXXXXX (light/dark)
```

**Spacing Scale:**
```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
xxl: 48px
```

**Layout Approach:**
- Grid system
- Responsive breakpoints
- Component spacing

**Motion Strategy:**
- Transitions
- Animations
- Loading states

4. **Propose safe choices AND creative risks**

```
SAFE CHOICES (match category expectations):
- [Safe choice 1]
- [Safe choice 2]

RISKS (where you'd stand out):
- [Creative risk 1] - Why it's different
- [Creative risk 2] - Why it works
```

5. **Generate preview**

Create an interactive HTML preview showing realistic pages in the design system.

6. **Output**

Create `DESIGN.md` with full design system specification.

## Mode 2: Design Review (80-Item Audit)

### When to Use

After implementation, audit the live site.

### The 80-Item Audit

#### Information Architecture (10 items)
- [ ] Clear content hierarchy (H1, H2, H3)
- [ ] Consistent heading scale
- [ ] Appropriate use of white space
- [ ] Content prioritization (primary/secondary/tertiary)
- [ ] Scannable text (short paragraphs, bullet points)
- [ ] Clear navigation structure
- [ ] Consistent terminology
- [ ] Breadcrumbs if deep hierarchy
- [ ] Search functionality if needed
- [ ] Empty states designed

#### Visual Design (20 items)
- [ ] Consistent typography scale
- [ ] Readable font sizes (min 16px for body)
- [ ] Appropriate line height (1.5-1.7 for body)
- [ ] Sufficient color contrast (WCAG AA)
- [ ] Consistent spacing scale
- [ ] Balanced visual weight
- [ ] Clear alignment
- [ ] Consistent border radius
- [ ] Consistent shadows
- [ ] Consistent icon style
- [ ] Image quality (no blurry, appropriate size)
- [ ] Professional color choices
- [ ] No jarring color combinations
- [ ] Consistent button styles
- [ ] Clear form styling
- [ ] Card styling consistency
- [ ] Table/list styling
- [ ] Loading states designed
- [ ] Error states styled
- [ ] Success feedback designed

#### Interaction Design (15 items)
- [ ] Hover states on all interactive elements
- [ ] Focus states for accessibility
- [ ] Active/pressed states
- [ ] Disabled states styled
- [ ] Loading indicators
- [ ] Transition animations
- [ ] Micro-interactions
- [ ] Smooth scrolling
- [ ] Back button works
- [ ] Forms can be submitted
- [ ] Confirmation dialogs
- [ ] Error messages clear
- [ ] Success messages clear
- [ ] Tooltips if needed
- [ ] Keyboard navigation works

#### Layout (15 items)
- [ ] Responsive breakpoints
- [ ] Mobile-first design
- [ ] Content fits viewport
- [ ] No horizontal scroll
- [ ] Images scale appropriately
- [ ] Videos embed correctly
- [ ] Navigation collapses on mobile
- [ ] Touch targets adequate size
- [ ] Cards stack on mobile
- [ ] Tables scroll on mobile
- [ ] Modal/cart fits screen
- [ ] Footer stays at bottom
- [ ] Sidebar collapses if needed
- [ ] Grid maintains alignment

#### AI Slop Detection (20 items)
- [ ] No gradient hero backgrounds
- [ ] No three-column icon grids
- [ ] No uniform 8px border radius everywhere
- [ ] No generic stock photos
- [ ] No \"Get Started\" CTAs
- [ ] No \"Hello, World\" hero text
- [ ] No rounded pill-shaped buttons everywhere
- [ ] No gradient text
- [ ] No floating cards with shadows
- [ ] No centered everything
- [ ] No excessive whitespace
- [ ] No blue/purple color schemes everywhere
- [ ] No \"clean, modern UI\" descriptions
- [ ] No placeholder images
- [ ] No generic illustrations
- [ ] No \"as a team\" language
- [ ] No \"powered by\" badges
- [ ] No \"© 2024\" in footer
- [ ] No \"Made with\" badges
- [ ] No \"Join our newsletter\" forms

## AI Slop Patterns

### The Big Three

| Pattern | AI Slop | Alternative |
|---------|---------|-------------|
| Hero | Gradient background | Bold typography, real image, solid color |
| Layout | Three-column icon grid | Asymmetric layout, two-column, masonry |
| Radius | Uniform 8px everywhere | Vary by element role (buttons 4px, cards 8px, modals 12px) |

### Typography Anti-Patterns

| Pattern | AI Slop | Alternative |
|---------|---------|-------------|
| Font | Only sans-serif | Mix serif for display, mono for data |
| Size | All 16px | Clear scale (14, 16, 20, 24, 32, 48) |
| Weight | All 400 | Use weight contrast (400 body, 600 headings, 700 emphasis) |

### Color Anti-Patterns

| Pattern | AI Slop | Alternative |
|---------|---------|-------------|
| Primary | Blue everywhere | Category-specific color |
| Accent | Purple/blue gradient | Single bold accent |
| Neutrals | Pure gray | Warm or cool grays |
| Background | Pure white | Off-white with slight warmth |

## Rating System

### Per-Category Rating

Rate each category 0-10:

| Score | Meaning | Action |
|-------|---------|--------|
| 0-2 | Severe issues | Major rework needed |
| 3-4 | Many issues | Significant fixes |
| 5-6 | Some issues | Targeted fixes |
| 7-8 | Minor issues | Polish pass |
| 9-10 | Excellent | Quick review only |

### What a 10 Looks Like

```
Information Architecture: 10/10
- Clear hierarchy that guides the eye
- Content prioritized perfectly
- Easy to scan and find information

Visual Design: 10/10
- Consistent and intentional
- No generic patterns
- Unique identity

Interaction Design: 10/10
- Every state designed
- Smooth transitions
- Delightful micro-interactions

Layout: 10/10
- Responsive and balanced
- No awkward breakpoints
- Professional on all devices

AI Slop: 10/10
- No recognizable AI patterns
- Intentional design choices
- Stands out from templates
```

## Output

### Design System Document (DESIGN.md)

```markdown
# Design System: [Project Name]

## Aesthetic Direction
[Description of the overall feel]

## Typography
- Display: [Font]
- Body: [Font]
- Mono: [Font]

## Color Palette
[Full color palette with hex values]

## Spacing Scale
[Spacing system]

## Layout
[Grid and responsive approach]

## Motion
[Animation guidelines]

## Component Guidelines
[How to use design system]

## AI Slop Avoidance Checklist
[What to avoid]
```

### Design Review Report

```markdown
# Design Review Report

## Overall Score: X/10

## By Category

| Category | Score | Issues |
|----------|-------|--------|
| Info Architecture | 8/10 | 2 minor |
| Visual Design | 6/10 | 4 issues |
| ... | | |

## Issues Found

### HIGH Priority
1. [Issue with file location]
2. [Fix recommendation]

### MEDIUM Priority
1. [Issue]
2. [Fix]

### LOW Priority
1. [Polish items]
```

## Integration with VIC-SDD

1. After design consultation: Create `DESIGN.md`
2. After design review: Generate fix commits
3. Update `SPEC-ARCHITECTURE.md` with design decisions

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `vibe-architect` | Design decisions in architecture spec |
| `vibe-qa` | Verify design implementation via e2e tests |
| `pre-decision-check` | Design quality gate before release |
| `spec-architect` | Integrate design into SPEC contracts |

---

## Invocation

```bash
# Design consultation
skill vibe-design
# "Help me build a design system for..."

# Design review
skill vibe-design
# "Review the design of my app"
```

---

## Pipeline Metadata

pipeline_metadata:
  handoff:
    delivers:
      - artifact: "DESIGN.md"
        description: "Design system specification (typography, colors, spacing, motion)"
      - artifact: "design review report (markdown)"
        description: "80-item audit results with per-category scores (0-10)"
    consumes:
      - artifact: "SPEC-ARCHITECTURE.md"
        description: "Architecture context"
      - artifact: "implemented UI/code (for review mode)"
        description: "What to audit"
  exit_condition:
    success: "Design system complete (build mode) or audit complete with scores (review mode)"
    failure: "Critical design issues found — fix before proceeding"
    triggers_next_on_success: "implementation or vibe-qa (E2E testing)"
    triggers_next_on_failure: "implementation (fix critical issues)"
  agent_pattern: Generator
