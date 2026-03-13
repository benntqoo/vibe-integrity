---
name: vibe-design
description: AI-assisted requirement clarification and design helper that automatically updates project architecture memory through structured dialogue
---

# Vibe Design

## Overview

Vibe Design is a requirement clarification and design helper that guides users through structured dialogue to refine ideas, clarify requirements, and make architectural decisions. Unlike generic brainstorming tools, Vibe Design automatically records decisions and insights into the project's `.vibe-integrity/` architecture memory system, ensuring that AI-assisted development maintains a coherent project memory without manual documentation overhead.

## Core Philosophy

**AI should remember what it learns during collaboration**, not rely on humans to manually update project documentation. Vibe Design achieves this by:

1. **Structured Dialogue**: Using targeted questioning (inspired by Socratic methods) to clarify user intent
2. **Automatic Architecture Memory Updates**: Recording decisions directly to `.vibe-integrity/` YAML files as they're made
3. **Conflict Avoidance**: Designed to work standalone or with vibe-coding approaches, with clear guidance about avoiding confusion with TDD/SDD workflows
4. **Progressive Disclosure**: Presenting information in digestible chunks with validation at each step

## When to Use

Use Vibe Design when:
- A user presents an idea, feature request, or problem statement that needs clarification
- You need to help users distinguish between essential requirements and nice-to-haves
- Architectural or technical decisions need to be made and recorded
- You want to ensure AI maintains accurate project memory throughout the conversation
- The goal is to create a shared understanding before implementation begins

**Do NOT use when**:
- The user has already provided clear, implementable specifications
- You're in the middle of implementing a previously agreed-upon plan
- The team is actively following TDD or SDD methodologies (to avoid workflow confusion)
- You need to perform code analysis or debugging (use other skills for those purposes)

## How It Works

### The Clarification Process

Vibe Design follows a structured approach:

1. **Context Establishment**: First understands what already exists in the project
2. **Progressive Questioning**: Asks one focused question at a time to avoid overwhelming the user
3. **Decision Capture**: When users make choices, automatically records them to appropriate `.vibe-integrity/` files:
   - Technical decisions → `tech-records.yaml`
   - Data model changes → `schema-evolution.yaml` 
   - Module/dependency discussions → `dependency-graph.yaml` and `module-map.yaml`
   - Risk identification → `risk-zones.yaml`
   - Project scope/goals → `project.yaml`
4. **Incremental Validation**: Presents understanding in sections and validates with the user before proceeding
5. **Summary Generation**: Creates a coherent design summary that reflects all captured decisions

### Automatic Architecture Memory Updates

As decisions are made during the dialogue, Vibe Design uses the `vibe-integrity-writer` skill to safely update:

| Decision Type | Updated File | Example |
|---------------|--------------|---------|
| Technical architecture choice | `tech-records.yaml` | "Selected PostgreSQL over MongoDB for relational data needs" |
| Data model modification | `schema-evolution.yaml` | "Added user_preferences table with JSONB column for settings" |
| New module introduction | `dependency-graph.yaml` | "Added auth-service module depending on user-service" |
| Structural reorganization | `module-map.yaml` | "Moved utility functions to shared/lib directory" |
| Identified risk area | `risk-zones.yaml` | "Payment processing integration identified as high-risk due to PCI compliance" |
| Project goal refinement | `project.yaml` | "Updated description to reflect focus on real-time analytics" |

## Key Differences from Brainstorming

While Vibe Design shares some similarities with brainstorming techniques, it differs in critical ways:

| Aspect | Vibe Design | Generic Brainstorming |
|--------|-------------|----------------------|
| **Primary Goal** | Clarify requirements + Update project memory | Generate ideas |
| **Question Approach** | Targeted, one-at-a-time, validation-focused | Often exploratory, multiple angles |
| **Output** | Structured decisions recorded to YAML | Free-form ideas, notes |
| **Integration** | Direct updates to `.vibe-integrity/` | Manual documentation required |
| **Workflow Fit** | Designed for AI-assisted development clarity | General purpose ideation |
| **Conflict Avoidance** | Explicit guidance about TDD/SDD separation | No specific workflow guidance |

## Integration Guidelines

### Working Alongside Vibe Integrity

Vibe Design is a complementary skill to the core Vibe Integrity system:
- Use Vibe Design **during the clarification phase** to understand what needs to be built
- Use Vibe Guard (`validate-vibe-guard.py`) **after implementation claims** to verify completion
- The two skills form a complete loop: Clarify → Build → Verify

### Avoiding Workflow Confusion

To prevent AI confusion, follow these guidelines:

1. **Explicit Workflow Declaration**: At the start of a session, clarify which approach is being used:
   - "We're using Vibe Design for clarification today"
   - "We're following TDD with Vibe Integrity for verification"

2. **Separate Sessions**: Consider using different git worktrees or sessions for different workflows:
   - One session for Vibe Design clarification work
   - Another for TDD/SDD implementation with appropriate skills

3. **Clear Handoffs**: When transitioning from clarification to implementation:
   - Summarize what was decided and recorded in `.vibe-integrity/`
   - Explicitly state: "Now switching to [TDD/SDD/vibe-coding] implementation mode"

## Output Format

Vibe Design produces two key artifacts:

1. **Updated Architecture Memory**: Automatic updates to `.vibe-integrity/` YAML files as decisions are made
2. **Design Summary Document**: A consolidated markdown file saved to `docs/plans/YYYY-MM-DD-<topic>-design.md` containing:
   - Clarified problem statement
   - Key decisions made (with references to YAML records)
   - Open questions or areas needing further clarification
   - Suggested next steps

## Implementation Notes

Vibe Design avoids generating implementation code directly. Its purpose is strictly:
- Requirement clarification
- Decision recording
- Creating shared understanding

Once a design is clarified and recorded, users can proceed with implementation using whatever approach they prefer (vibe-coding, TDD, SDD, etc.), with confidence that the project's architecture memory accurately reflects the agreed-upon direction.

## Machine-Readable Outputs

All decisions made during Vibe Design sessions are recorded as structured data in the `.vibe-integrity/` directory, making them:
- Queryable by other AI sessions
- Auditable for compliance and tracking
- Usable for generating documentation
- Suitable for feeding into automated architecture diagrams