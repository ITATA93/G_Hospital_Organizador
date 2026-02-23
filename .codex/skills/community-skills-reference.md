# Community Claude Skills Reference

A curated list of community Claude Skills and resources.

## Official Skills (Anthropic)

### Document Skills
| Skill | Description |
|-------|-------------|
| [docx](https://github.com/anthropics/skills/tree/main/skills/docx) | Create, edit, and analyze Word documents |
| [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) | PDF manipulation toolkit |
| [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) | PowerPoint presentations |
| [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) | Excel spreadsheets |

### Design & Creative
| Skill | Description |
|-------|-------------|
| [algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art) | Generative art with p5.js |
| [canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | Visual art design |
| [slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator) | Animated GIFs for Slack |

### Development
| Skill | Description |
|-------|-------------|
| [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design) | Bold frontend design decisions |
| [mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | Create MCP servers |
| [webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | Test web apps with Playwright |
| [web-artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | Build HTML artifacts |

### Communication
| Skill | Description |
|-------|-------------|
| [brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | Apply brand colors/typography |
| [internal-comms](https://github.com/anthropics/skills/tree/main/skills/internal-comms) | Write internal communications |

### Skill Creation
| Skill | Description |
|-------|-------------|
| [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Interactive skill creation tool |

---

## Community Collections

### obra/superpowers
**[GitHub](https://github.com/obra/superpowers)** - Core skills library with 20+ battle-tested skills

Features:
- `/brainstorm`, `/write-plan`, `/execute-plan` commands
- TDD, debugging, and collaboration patterns
- skills-search tool

Install: `/plugin marketplace add obra/superpowers-marketplace`

### obra/superpowers-lab
**[GitHub](https://github.com/obra/superpowers-lab)** - Experimental skills for Superpowers

---

## Individual Community Skills

| Skill | Description |
|-------|-------------|
| [ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill) | iOS app building and testing automation |
| [ffuf-web-fuzzing](https://github.com/jthack/ffuf_claude_skill) | Web fuzzing for pentesting |
| [playwright-skill](https://github.com/lackeyjb/playwright-skill) | General Playwright automation |
| [claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill) | D3.js visualizations |
| [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | Scientific libraries and databases |
| [web-asset-generator](https://github.com/alonw0/web-asset-generator) | Favicons, app icons, social images |
| [loki-mode](https://github.com/asklokesh/claudeskill-loki-mode) | Multi-agent startup system |
| [Trail of Bits Security](https://github.com/trailofbits/skills) | Security skills (CodeQL, Semgrep) |

---

## Tools

| Tool | Description |
|------|-------------|
| [Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | Convert documentation to Skills |

---

## Installing Skills

### Claude Code CLI
```bash
# From marketplace
/plugin marketplace add anthropics/skills

# From local directory
/plugin add /path/to/skill-directory
```

### Claude.ai Web
1. Settings > Capabilities
2. Enable Skills toggle
3. Browse or upload skills

---

## Creating Your Own Skill

### Structure
```
my-skill/
├── SKILL.md          # Main skill file with frontmatter
├── scripts/          # Optional executable scripts
└── resources/        # Optional supporting files
```

### SKILL.md Format
```yaml
---
name: my-skill
description: Brief description for skill discovery
---

# Detailed Instructions

Claude will read these instructions when the skill is activated.

## Usage
...

## Examples
...
```

---

## Resources

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [VoltAgent Awesome Agent Skills](https://github.com/VoltAgent/awesome-agent-skills)
- [Claude Skills Spec](https://github.com/anthropics/skills/tree/main/spec)
