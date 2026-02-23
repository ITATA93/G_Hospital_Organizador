---
name: skill-creator
description: Create new Codex CLI skills with proper structure and documentation. Use this when the user wants to create a reusable skill for automating tasks, adding specialized capabilities, or extending Codex functionality.
---

# Skill Creator

## Overview

This skill helps create new Codex CLI skills with the correct structure, frontmatter, and documentation. Skills extend Codex capabilities for specialized tasks.

## When to Use

Use this skill when:
- User wants to create a new reusable skill
- Automating a repetitive workflow
- Adding specialized domain knowledge
- Creating project-specific agent capabilities

## Skill Structure

### Directory Layout
```
~/.codex/skills/
├── my-skill.md           # Simple single-file skill
└── complex-skill/        # Multi-file skill
    ├── SKILL.md          # Main skill file
    ├── references/       # Supporting documentation
    │   └── patterns.md
    └── assets/           # Templates, examples
        └── template.txt
```

### Frontmatter Format
```yaml
---
name: skill-name        # Lowercase, hyphenated
description: Brief description of what the skill does and when to use it
---
```

### Content Sections

1. **Overview**: What the skill does
2. **When to Use**: Trigger conditions
3. **Core Workflow**: Step-by-step process
4. **Best Practices**: Do's and don'ts
5. **Resources**: References to supporting files

## Creating a New Skill

### Step 1: Define Purpose
Ask the user:
- What task should this skill automate?
- What inputs does it need?
- What outputs should it produce?
- Are there existing patterns to follow?

### Step 2: Create the File
```bash
# Simple skill
touch ~/.codex/skills/my-skill.md

# Complex skill with references
mkdir -p ~/.codex/skills/my-skill/{references,assets}
touch ~/.codex/skills/my-skill/SKILL.md
```

### Step 3: Write the Skill

Template for a new skill:
```markdown
---
name: {skill-name}
description: {One sentence describing the skill and when to use it}
---

# {Skill Display Name}

## Overview

{2-3 sentences explaining what this skill does}

## When to Use

Use this skill when:
- {Condition 1}
- {Condition 2}
- {Condition 3}

## Core Workflow

### 1. {First Step}
{Instructions}

### 2. {Second Step}
{Instructions}

### 3. {Third Step}
{Instructions}

## Best Practices

- {Practice 1}
- {Practice 2}
- {Practice 3}

## Examples

### Example 1: {Description}
{Code or command example}

### Example 2: {Description}
{Code or command example}
```

### Step 4: Test the Skill
```bash
codex exec "Use the {skill-name} skill to {task}"
```

## Skill Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **Development** | Code generation, testing | test-generator, api-builder |
| **Documentation** | Docs, changelogs | doc-writer, changelog-updater |
| **Analysis** | Code review, audits | security-review, perf-analyzer |
| **Automation** | CI/CD, deployment | deploy-helper, release-manager |
| **Research** | Information gathering | web-researcher, api-explorer |

## Best Practices

### DO
- Keep skills focused on one task
- Include clear trigger conditions
- Provide examples in the skill
- Use references for large code blocks

### DON'T
- Create overly broad skills
- Include secrets or credentials
- Duplicate existing Codex capabilities
- Make skills dependent on specific projects

## Skill Naming Conventions

- Use lowercase with hyphens: `my-skill-name`
- Be descriptive but concise
- Avoid generic names like `helper` or `util`
- Include domain if specialized: `react-component-generator`

## Output

After creating a skill, report:
1. File path created
2. Skill name and description
3. How to invoke the skill
4. Suggested test command
