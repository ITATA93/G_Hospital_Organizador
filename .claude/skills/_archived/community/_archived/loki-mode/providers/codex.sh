#!/bin/bash
# OpenAI Codex CLI Provider Configuration
# Shell-sourceable config for loki-mode multi-provider support

# Provider Functions (for external use)
# =====================================
# These functions provide a clean interface for external scripts:
#   provider_detect()           - Check if CLI is installed
#   provider_version()          - Get CLI version
#   provider_invoke()           - Invoke with prompt (autonomous mode)
#   provider_invoke_with_tier() - Invoke with tier-specific effort level
#   provider_get_tier_param()   - Map tier name to effort level
#
# Usage:
#   source providers/codex.sh
#   if provider_detect; then
#       provider_invoke "Your prompt here"
#   fi
#
# Note: autonomy/run.sh uses inline invocation for streaming support
# and real-time agent tracking. These functions are intended for
# simpler scripts, wrappers, and external integrations.
# =====================================

# Provider Identity
PROVIDER_NAME="codex"
PROVIDER_DISPLAY_NAME="OpenAI Codex CLI"
PROVIDER_CLI="codex"

# CLI Invocation
# Note: codex uses positional prompt after "exec" subcommand
# VERIFIED: exec --dangerously-bypass-approvals-and-sandbox confirmed in codex exec --help (v0.89.0)
# "Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY DANGEROUS."
PROVIDER_AUTONOMOUS_FLAG="exec --dangerously-bypass-approvals-and-sandbox"
PROVIDER_PROMPT_FLAG=""
PROVIDER_PROMPT_POSITIONAL=true

# Skill System (2026 UPDATE: Codex now has skills)
PROVIDER_SKILL_DIR="~/.codex/skills"
PROVIDER_SKILL_FORMAT="markdown"

# Capability Flags (2026 UPDATE)
PROVIDER_HAS_SUBAGENTS=false      # Still no Task tool for parallel subagents
PROVIDER_HAS_PARALLEL=false       # Consequence of no Task tool
PROVIDER_HAS_TASK_TOOL=false      # ONLY real limitation
PROVIDER_HAS_MCP=true             # ✅ MCP support added 2026
PROVIDER_HAS_SKILLS=true          # ✅ Skills system (Jan 2026)
PROVIDER_HAS_WEB_SEARCH=true      # ✅ Integrated web search
PROVIDER_HAS_DEEP_RESEARCH=true   # ✅ Pro feature
PROVIDER_MAX_PARALLEL=1

# Model Configuration
# Codex uses single model with effort parameter
# NOTE: "gpt-5.2-codex" is a PLACEHOLDER model name. Update this value when
# official Codex CLI documentation specifies the actual model identifier.
PROVIDER_MODEL_PLANNING="gpt-5.2-codex"
PROVIDER_MODEL_DEVELOPMENT="gpt-5.2-codex"
PROVIDER_MODEL_FAST="gpt-5.2-codex"

# Effort levels (Codex-specific: maps to reasoning time, not model capability)
PROVIDER_EFFORT_PLANNING="xhigh"
PROVIDER_EFFORT_DEVELOPMENT="high"
PROVIDER_EFFORT_FAST="low"

# No Task tool - effort is set via CLI flag
PROVIDER_TASK_MODEL_PARAM=""
PROVIDER_TASK_MODEL_VALUES=()

# Context and Limits
PROVIDER_CONTEXT_WINDOW=128000
PROVIDER_MAX_OUTPUT_TOKENS=32000
PROVIDER_RATE_LIMIT_RPM=60

# Cost (USD per 1K tokens, approximate for GPT-5.2)
PROVIDER_COST_INPUT_PLANNING=0.010
PROVIDER_COST_OUTPUT_PLANNING=0.030
PROVIDER_COST_INPUT_DEV=0.010
PROVIDER_COST_OUTPUT_DEV=0.030
PROVIDER_COST_INPUT_FAST=0.010
PROVIDER_COST_OUTPUT_FAST=0.030

# Partial Mode (2026 UPDATE: Only Task tool missing)
PROVIDER_DEGRADED=false
PROVIDER_PARTIAL=true
PROVIDER_PARTIAL_REASONS=(
    "No Task tool - cannot spawn parallel subagents (ONLY limitation)"
)
# 2026 CAPABILITIES NOW AVAILABLE:
# ✅ MCP server integration (config in ~/.codex/config.toml)
# ✅ Native skills system (Jan 2026 feature)
# ✅ Web search (integrated)
# ✅ Deep research (Pro license)

# Detection function - check if provider CLI is available
provider_detect() {
    command -v codex >/dev/null 2>&1
}

# Version check function
provider_version() {
    codex --version 2>/dev/null | head -1
}

# Invocation function
# Note: Codex uses positional prompt, not -p flag
# Note: Reasoning effort is configured via environment or config, not CLI flag
provider_invoke() {
    local prompt="$1"
    shift
    codex exec --dangerously-bypass-approvals-and-sandbox "$prompt" "$@"
}

# Model tier to effort level parameter (Codex uses effort, not separate models)
provider_get_tier_param() {
    local tier="$1"
    case "$tier" in
        planning) echo "xhigh" ;;
        development) echo "high" ;;
        fast) echo "low" ;;
        *) echo "high" ;;  # default to development tier
    esac
}

# Tier-aware invocation
# Note: Codex CLI does not support effort CLI flags
# Effort must be configured via environment: CODEX_MODEL_REASONING_EFFORT
# This function sets the env var before invocation
provider_invoke_with_tier() {
    local tier="$1"
    local prompt="$2"
    shift 2
    local effort
    effort=$(provider_get_tier_param "$tier")
    CODEX_MODEL_REASONING_EFFORT="$effort" codex exec --dangerously-bypass-approvals-and-sandbox "$prompt" "$@"
}

# =============================================================================
# PRO LICENSE FEATURES (2026)
# =============================================================================
# Available with OpenAI Pro subscription:
#   - gpt-5.1-codex-max: Extended context (256K), enhanced reasoning
#   - Deep Research: Extended research mode with citations
#   - Priority Queue: Faster response times
#   - Extended Context: 256K tokens vs 128K standard

PROVIDER_PRO_MODEL="gpt-5.1-codex-max"
PROVIDER_PRO_CONTEXT=256000
PROVIDER_PRO_FEATURES=(
    "deep_research"
    "extended_context"
    "priority_queue"
    "full_citations"
)

# Pro-tier invocation with max model
provider_invoke_pro() {
    local prompt="$1"
    shift
    CODEX_MODEL="gpt-5.1-codex-max" codex exec --dangerously-bypass-approvals-and-sandbox "$prompt" "$@"
}

# Deep research invocation (Pro only)
provider_invoke_deep_research() {
    local prompt="$1"
    shift
    codex exec --deep-research --dangerously-bypass-approvals-and-sandbox "$prompt" "$@"
}
