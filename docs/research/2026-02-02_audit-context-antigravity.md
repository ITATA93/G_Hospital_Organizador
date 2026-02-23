---
date: 2026-02-02
topic: Audit Context Building - Antigravity Workspace
researcher: claude-opus
method: trail-of-bits-audit-context-building
sources_count: 15+
---

# Audit Context: Antigravity Workspace

## Executive Summary

Antigravity Workspace is a **multi-vendor AI agent orchestration system** that provides:
- Unified configuration management for 3 AI CLI vendors (Gemini, Claude, Codex)
- 7 specialized sub-agents with automatic delegation
- Central library for agents/skills with symlink-based activation
- Global profile and project template system

This document provides deep architectural context before any vulnerability or improvement analysis.

---

## Phase 1: Initial Orientation

### 1.1 Major Modules

| Module | Location | Purpose |
|--------|----------|---------|
| **Vendor Configs** | `.gemini/`, `.claude/`, `.codex/` | Per-vendor agent and skill definitions |
| **Sub-agents** | `.subagents/` | Multi-vendor dispatch and manifest |
| **Global Profile** | `_global-profile/` | Shared configs installable to `~/` |
| **Template** | `_template/` | Project scaffolding for new projects |
| **Central Library** | `_global-profile/.antigravity/library/` | Reusable agents/skills with activation scripts |
| **Documentation** | `docs/` | Project docs, research, decisions |

### 1.2 Entrypoints

| Entrypoint | Type | Description |
|------------|------|-------------|
| `dispatch.sh` | Bash script | Multi-vendor agent dispatcher (L1-223) |
| `install-global.ps1/.sh` | Scripts | Deploy global profile to user home |
| `init-project.ps1/.sh` | Scripts | Create new project from template |
| `enable.sh/disable.sh/list.sh` | Library scripts | Manage agent/skill activation |

### 1.3 Actors

| Actor | Trust Level | Capabilities |
|-------|-------------|--------------|
| **User** | Trusted | Invokes agents, modifies configs |
| **Gemini CLI** | Semi-trusted | Executes prompts, file access |
| **Claude Code** | Semi-trusted | Full IDE integration, Task tool |
| **Codex CLI** | Semi-trusted | MCP, skills, no Task tool |
| **Sub-agents** | Constrained | Scoped per manifest instructions |

### 1.4 Key State Variables

| Variable | Location | Purpose |
|----------|----------|---------|
| `manifest.json` | `.subagents/` | Agent registry, vendors, triggers |
| `settings.json` | `.gemini/` | Memory, MCP, agent settings |
| `config.yaml` | `.codex/` | Effort levels, capabilities |
| `catalog.json` | `library/` | Central index of agents/skills |

---

## Phase 2: Component Deep Analysis

### 2.1 dispatch.sh — Multi-Vendor Dispatcher

**File:** [.subagents/dispatch.sh](.subagents/dispatch.sh)
**Lines:** 223

#### Purpose
Routes agent invocations to the correct vendor CLI based on manifest configuration and optional override. Central orchestration point for the multi-vendor system.

#### Inputs & Assumptions
- **$1** (agent_name): Must exist in manifest.json
- **$2** (prompt): User task/prompt string
- **$3** (vendor_override): Optional, must be gemini|claude|codex
- **Implicit**: `jq` installed, manifest.json valid JSON
- **Implicit**: Vendor CLIs installed and authenticated

#### Outputs & Effects
- Invokes one of: `gemini`, `claude`, or `codex exec`
- Displays Codex degraded mode warning when vendor=codex
- Exit codes: 0=success, 1=error

#### Block-by-Block Analysis

**L1-13: Header and usage**
- Standard bash script with `set -e` (fail-fast)
- *Invariant*: Script exits on first error

**L14-30: Configuration**
- Sets SCRIPT_DIR, WORKSPACE_ROOT, MANIFEST_PATH
- *Assumption*: Script is in `.subagents/` directory
- *5 Whys*: Why derive paths? → Portability across machines

**L31-39: Logging functions**
- Color-coded output (info, warn, error, success)
- *Invariant*: All user-facing messages go through these

**L41-63: show_usage()**
- Displays help text with available agents
- *First Principles*: Self-documenting CLI

**L65-82: show_codex_warning()**
- Displays degraded mode warning for Codex
- Lists limitations: no Task tool, sequential, no MCP
- **Note**: MCP claim outdated (Codex 2026 has MCP)
- *Risk*: Warning may mislead users about current capabilities

**L84-99: check_command()**
- Validates CLI tool exists
- Provides install instructions per vendor
- *Invariant*: Fails early if vendor not installed

**L102-116: get_agent_config() / get_codex_effort()**
- Extracts agent config from manifest using jq
- Defaults effort to "high" if not specified
- *Assumption*: manifest.json has valid structure

**L118-164: Argument validation**
- Checks minimum args, validates agent exists
- Validates vendor in supported_vendors list
- *Invariant*: Only valid agent+vendor combinations proceed

**L166-174: Prompt construction**
- Combines agent instructions with user prompt
- *5 Hows*: How does agent get context? → Instructions prepended

**L180-220: Vendor invocation**
- **Gemini**: `gemini --yolo "$FULL_PROMPT"`
  - *Risk*: `--yolo` bypasses confirmations
- **Claude**: `claude --dangerously-skip-permissions -p "$FULL_PROMPT"`
  - *Risk*: `--dangerously-skip-permissions` full access
- **Codex**: `CODEX_MODEL_REASONING_EFFORT="$EFFORT" codex exec --dangerously-bypass-approvals-and-sandbox "$FULL_PROMPT"`
  - *Risk*: Full sandbox bypass

#### Cross-Function Dependencies
- **Reads**: manifest.json
- **Invokes**: External CLIs (gemini, claude, codex)
- **Shared state**: None (stateless script)

#### Invariants
1. Only agents defined in manifest can be invoked
2. Only supported vendors per agent are allowed
3. Script fails fast on any error
4. All invocations use autonomous/bypass flags

#### Assumptions
1. User has authenticated all 3 CLIs
2. manifest.json is valid JSON with correct schema
3. jq is installed
4. Vendor CLIs are in PATH
5. Working directory is workspace root

#### Risks
1. **Bypass flags**: All vendors invoked with maximum permissions
2. **No sandboxing**: Agents have full system access
3. **Outdated warnings**: Codex warning mentions no MCP (incorrect for 2026)
4. **No rate limiting**: Could exhaust API quotas
5. **No output validation**: Agent output not validated

---

### 2.2 manifest.json — Agent Registry

**File:** [.subagents/manifest.json](.subagents/manifest.json)
**Lines:** 155

#### Purpose
Central registry defining all agents, their default vendors, supported vendors, triggers, and per-vendor configurations.

#### Structure Analysis

**L1-17: Header and vendors**
```json
{
  "version": "2.0",
  "vendors": {
    "available": ["gemini", "claude", "codex"],
    "default": "gemini",
    "codex_partial": true
  }
}
```
- *Invariant*: Default vendor must be in available list
- *Assumption*: All 3 vendors are installed

**L18-152: Agents array**

| Agent | Default Vendor | Scope | Key Triggers |
|-------|---------------|-------|--------------|
| code-analyst | gemini | project | analyze, architecture |
| doc-writer | gemini | project | document, README |
| code-reviewer | claude | project | review, security |
| test-writer | gemini | project | test, coverage |
| db-analyst | claude | project | database, SQL |
| deployer | gemini | project | deploy, docker |
| researcher | codex | global | research, best practices |

#### Per-Agent Configuration Pattern
```json
{
  "name": "agent-name",
  "vendor": "default-vendor",
  "supported_vendors": ["gemini", "claude", "codex"],
  "scope": "project|global",
  "triggers": ["keyword1", "keyword2"],
  "instructions": "Agent system prompt",
  "codex_config": { "effort": "high|xhigh|medium|low" },
  "claude_config": { "model": "opus|sonnet", "allow_parallel": true },
  "gemini_config": { "model": "pro|flash", "thinking_mode": true }
}
```

#### Invariants
1. Each agent has unique name
2. Default vendor must be in supported_vendors
3. All agents support all 3 vendors (redundant but explicit)
4. Instructions are read-only guidance

#### Assumptions
1. Trigger keywords are mutually exclusive across agents
2. Instructions are sufficient for agent behavior
3. Config values are valid for each vendor

#### Risks
1. **Trigger overlap**: "audit" could match code-reviewer OR db-analyst
2. **Instructions too brief**: May not constrain behavior sufficiently
3. **No validation schema enforcement**: Runtime failures possible

---

### 2.3 Library Activation System

**Files:**
- [enable.sh](library/scripts/enable.sh) (117 lines)
- [disable.sh](library/scripts/disable.sh) (96 lines)
- [list.sh](library/scripts/list.sh) (125 lines)

#### Purpose
Symlink-based activation system allowing agents/skills from central library to be enabled per-vendor.

#### enable.sh Flow
```
1. Validate args (type, name, vendor)
2. Check source exists in library/agents|skills/
3. Create target directory ~/.{vendor}/agents|skills/
4. Create symlink: target → source
```

#### disable.sh Flow
```
1. Validate args
2. Check if target is symlink
3. Remove symlink (refuses if not symlink)
```

#### Invariants
1. Only symlinks are managed (never overwrites real files)
2. Source must exist in library
3. Target directories created if missing

#### Assumptions
1. User has write access to ~/
2. Symlinks work on filesystem
3. Vendors read from standard paths

#### Risks
1. **Windows compatibility**: Symlinks require admin or developer mode
2. **Path conflicts**: Existing files not overwritten (backup created)
3. **No atomic operations**: Partial states possible on error

---

## Phase 3: Global System Understanding

### 3.1 State & Invariant Map

```
┌────────────────────────────────────────────────────────────────┐
│                    SYSTEM STATE FLOW                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  catalog.json ─────┐                                           │
│  (library index)   │                                           │
│                    ▼                                           │
│  enable.sh ────► ~/.{vendor}/agents/*.md                       │
│                    │                                           │
│                    ▼                                           │
│  manifest.json ──► dispatch.sh ──► vendor CLI ──► AI Response  │
│  (agent config)         │                                      │
│                         │                                      │
│  .{vendor}/settings ────┘                                      │
│  (vendor config)                                               │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 3.2 Trust Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│ TRUST ZONE 1: User Space                                    │
│  - Configuration files                                       │
│  - Manifest definitions                                      │
│  - Documentation                                             │
├─────────────────────────────────────────────────────────────┤
│ TRUST ZONE 2: Script Execution                              │
│  - dispatch.sh (elevated via bypass flags)                   │
│  - enable/disable/list.sh                                    │
│  - install scripts                                           │
├─────────────────────────────────────────────────────────────┤
│ TRUST ZONE 3: AI Agent Execution (UNTRUSTED)                │
│  - Gemini CLI with --yolo                                    │
│  - Claude with --dangerously-skip-permissions                │
│  - Codex with --dangerously-bypass-approvals-and-sandbox     │
│                                                              │
│  ⚠️ Agents have FULL system access                           │
│  ⚠️ No sandboxing or output validation                       │
│  ⚠️ Relies entirely on agent instructions for constraints    │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Data Flow Diagram

```
User Request
     │
     ▼
┌─────────────┐
│ dispatch.sh │
└─────┬───────┘
      │
      ▼
┌─────────────────┐     ┌────────────────┐
│ manifest.json   │────►│ Agent Config   │
└─────────────────┘     └───────┬────────┘
                                │
      ┌─────────────────────────┼─────────────────────────┐
      │                         │                         │
      ▼                         ▼                         ▼
┌──────────┐            ┌──────────┐              ┌──────────┐
│  Gemini  │            │  Claude  │              │  Codex   │
│   CLI    │            │   Code   │              │   CLI    │
└────┬─────┘            └────┬─────┘              └────┬─────┘
     │                       │                         │
     ▼                       ▼                         ▼
┌──────────┐            ┌──────────┐              ┌──────────┐
│ Response │            │ Response │              │ Response │
│ (stdio)  │            │ (stdio)  │              │ (stdio)  │
└──────────┘            └──────────┘              └──────────┘
```

### 3.4 Complexity & Fragility Clusters

| Area | Complexity | Fragility | Reason |
|------|------------|-----------|--------|
| **dispatch.sh** | Medium | Medium | Multiple vendor paths, bypass flags |
| **manifest.json** | Low | Low | Static config, schema validated |
| **Library symlinks** | Low | High | Windows compatibility, permissions |
| **Codex warnings** | Low | Medium | Outdated information (MCP available) |
| **Memory system** | Medium | High | .gemini/brain/ empty, not functioning |
| **Research storage** | Low | Low | Simple file writes to docs/research/ |

---

## Documented Invariants

### System-Wide Invariants
1. **I1**: All agent invocations go through dispatch.sh or direct CLI
2. **I2**: Manifest is single source of truth for agent definitions
3. **I3**: Library activation uses symlinks only (never copies)
4. **I4**: Each agent has explicit read/write permissions in instructions
5. **I5**: Default vendor used unless override specified

### Security Invariants
1. **S1**: All vendor CLIs invoked with bypass flags (NO SANDBOXING)
2. **S2**: db-analyst requires confirmation for DELETE/DROP/UPDATE
3. **S3**: Agents receive instructions as system prompt context
4. **S4**: No credential storage in configuration files

### Data Flow Invariants
1. **D1**: Research output goes to docs/research/
2. **D2**: Memory (if working) goes to .gemini/brain/
3. **D3**: Logs (if enabled) go to .gemini/agents/logs/

---

## Documented Assumptions

### Configuration Assumptions
1. **A1**: User has all 3 CLIs installed and authenticated
2. **A2**: jq is installed for JSON processing
3. **A3**: Bash is available (or Git Bash on Windows)
4. **A4**: Symlinks work (Windows needs developer mode)

### Behavioral Assumptions
1. **A5**: Agents follow their instructions (no enforcement)
2. **A6**: Trigger keywords are sufficient for agent selection
3. **A7**: Effort levels correctly map to reasoning quality
4. **A8**: Codex has MCP support (contradicts warning in dispatch.sh)

### Integration Assumptions
1. **A9**: Global profile can be copied to ~/
2. **A10**: Template produces working project structure
3. **A11**: Vendor configs don't conflict with user configs

---

## Unresolved Questions

1. **Q1**: Why is .gemini/brain/ empty if memory.persistent=true?
2. **Q2**: Should dispatch.sh warning about Codex MCP be updated?
3. **Q3**: How are trigger conflicts resolved (multiple agents match)?
4. **Q4**: What validates agent output before returning to user?
5. **Q5**: Is there rate limiting or quota management?

---

## Metadata

- **Audit Date:** 2026-02-02
- **Methodology:** Trail of Bits audit-context-building
- **Agent:** Claude Code (Opus 4.5)
- **Scope:** Architectural context only (no vulnerability findings)
- **Files Analyzed:** 15+ configuration and script files
- **Phase:** Pre-vulnerability discovery
