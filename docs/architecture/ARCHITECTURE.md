# Architecture — Antigravity Development Environment

## Overview

Antigravity is a multi-agent development environment that combines Gemini CLI and Claude Code for AI-assisted software development.

```
┌─────────────────────────────────────────────────────────────┐
│                    ANTIGRAVITY SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │  Gemini CLI │◄───────►│ Claude Code │                   │
│  │  (Orchestr) │         │ (Sub-agent) │                   │
│  └──────┬──────┘         └─────────────┘                   │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────┐                   │
│  │         SUB-AGENTS (6)              │                   │
│  ├─────────────────────────────────────┤                   │
│  │ code-analyst  │ doc-writer          │                   │
│  │ code-reviewer │ test-writer         │                   │
│  │ db-analyst    │ deployer            │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Global Profile (`~/.gemini/`, `~/.claude/`)

Shared configuration installed in user home directory:
- Agent definitions (TOML)
- Behavioral rules (Markdown)
- Workflows (Markdown)
- Skills (Markdown)
- Commands (TOML/Markdown)

### 2. Project Template (`_template/`)

Quick-start for new projects with:
- Pre-configured Gemini and Claude settings
- Sub-agent manifest
- Documentation structure
- Standard directory layout

### 3. Sub-Agents

| Agent | Vendor | Specialty |
|-------|--------|-----------|
| code-analyst | Gemini | Code analysis, architecture review |
| doc-writer | Gemini | Documentation maintenance |
| code-reviewer | Gemini | Code review, security audit |
| test-writer | Gemini | Test generation |
| db-analyst | Gemini | Database analysis, SQL |
| deployer | Gemini | CI/CD, deployment |

### 4. Delegation Protocol

```
User Request
     │
     ▼
┌────────────┐
│  Trigger   │──► Detect keywords matching sub-agent
│ Detection  │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  Context   │──► Prepare briefing with relevant files
│ Preparation│
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Invocation │──► gemini -a {agent} --yolo --sandbox seatbelt
└─────┬──────┘
      │
      ▼
┌────────────┐
│Verification│──► Check output, retry if needed (max 2)
└────────────┘
```

## Security Rules

1. **Database Safety**: Never execute DELETE, DROP, UPDATE, TRUNCATE without confirmation
2. **Sandbox Mode**: All agents run with `--sandbox seatbelt`
3. **No Credentials**: Never expose API keys or passwords in code
4. **Read First**: Always read existing code before modifying

## File Organization

```
project/
├── .gemini/           → Gemini CLI config
│   ├── agents/        → Sub-agent definitions
│   ├── rules/         → Behavioral rules
│   ├── skills/        → Custom skills
│   ├── workflows/     → Session workflows
│   ├── commands/      → Custom commands
│   └── scripts/       → Utility scripts
├── .claude/           → Claude Code config
│   ├── commands/      → Slash commands
│   └── skills/        → Skills library
├── .agent/            → Agent rules
├── .subagents/        → Sub-agent manifest
├── src/               → Source code
├── tests/             → Test suites
├── docs/              → Documentation
├── scripts/           → Project scripts
├── config/            → Configuration files
├── GEMINI.md          → Gemini instructions
├── CLAUDE.md          → Claude instructions
└── CHANGELOG.md       → Version history
```

## Workflows

### Session Start
1. Read DEVLOG.md (last entry)
2. Read TODO.md (pending tasks)
3. Show git status and recent commits
4. Present executive summary

### Session End
1. Update DEVLOG.md with work done
2. Update TODO.md with new tasks
3. Update CHANGELOG.md if needed
4. Commit changes with descriptive message

### Parallel Execution
- Maximum 4 agents simultaneously
- Each agent works on different files
- Results aggregated after completion
- Logs saved to `.gemini/agents/logs/`
