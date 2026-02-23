#!/bin/bash
#
# list.sh - List available and enabled agents/skills
#
# Usage:
#   ./list.sh              # List all
#   ./list.sh agents       # List agents only
#   ./list.sh skills       # List skills only
#   ./list.sh status       # Show enabled status per vendor
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

# Check if enabled for vendor
is_enabled() {
    local type="$1"
    local name="$2"
    local vendor="$3"
    local target_dir

    case "$vendor" in
        gemini)
            [ "$type" = "agent" ] && target_dir="$HOME/.gemini/agents" || target_dir="$HOME/.gemini/skills"
            ;;
        claude)
            [ "$type" = "agent" ] && target_dir="$HOME/.claude/agents" || target_dir="$HOME/.claude/skills"
            ;;
        codex)
            [ "$type" = "agent" ] && target_dir="$HOME/.codex/agents" || target_dir="$HOME/.codex/skills"
            ;;
    esac

    [ -e "$target_dir/${name}.md" ] && echo "✓" || echo "·"
}

list_agents() {
    echo -e "${CYAN}=== AGENTS ===${NC}"
    echo ""
    printf "%-15s %-10s %-8s %-8s %-8s\n" "NAME" "DEFAULT" "GEMINI" "CLAUDE" "CODEX"
    printf "%-15s %-10s %-8s %-8s %-8s\n" "---------------" "----------" "--------" "--------" "--------"

    for file in "$LIBRARY_DIR/agents"/*.md; do
        [ -f "$file" ] || continue
        name=$(basename "$file" .md)

        # Get default vendor from catalog.json if exists
        default="?"
        if [ -f "$LIBRARY_DIR/catalog.json" ]; then
            default=$(grep -A1 "\"name\": \"$name\"" "$LIBRARY_DIR/catalog.json" 2>/dev/null | grep "default_vendor" | sed 's/.*: "\([^"]*\)".*/\1/' | head -1)
            [ -z "$default" ] && default="?"
        fi

        gemini_status=$(is_enabled "agent" "$name" "gemini")
        claude_status=$(is_enabled "agent" "$name" "claude")
        codex_status=$(is_enabled "agent" "$name" "codex")

        printf "%-15s %-10s %-8s %-8s %-8s\n" "$name" "$default" "$gemini_status" "$claude_status" "$codex_status"
    done
    echo ""
}

list_skills() {
    echo -e "${CYAN}=== SKILLS ===${NC}"
    echo ""
    printf "%-20s %-8s %-8s %-8s\n" "NAME" "GEMINI" "CLAUDE" "CODEX"
    printf "%-20s %-8s %-8s %-8s\n" "--------------------" "--------" "--------" "--------"

    for file in "$LIBRARY_DIR/skills"/*.md; do
        [ -f "$file" ] || continue
        name=$(basename "$file" .md)

        gemini_status=$(is_enabled "skill" "$name" "gemini")
        claude_status=$(is_enabled "skill" "$name" "claude")
        codex_status=$(is_enabled "skill" "$name" "codex")

        printf "%-20s %-8s %-8s %-8s\n" "$name" "$gemini_status" "$claude_status" "$codex_status"
    done
    echo ""
}

show_help() {
    echo "Antigravity Library Manager"
    echo ""
    echo "Usage:"
    echo "  $0              List all agents and skills"
    echo "  $0 agents       List agents only"
    echo "  $0 skills       List skills only"
    echo "  $0 help         Show this help"
    echo ""
    echo "Legend:"
    echo "  ✓  Enabled for vendor"
    echo "  ·  Not enabled"
    echo ""
    echo "To enable/disable:"
    echo "  ./enable.sh agent <name> <vendor>"
    echo "  ./disable.sh agent <name> <vendor>"
}

case "${1:-all}" in
    agents)
        list_agents
        ;;
    skills)
        list_skills
        ;;
    help|--help|-h)
        show_help
        ;;
    all|*)
        list_agents
        list_skills
        echo -e "${YELLOW}Legend: ✓ = enabled, · = not enabled${NC}"
        ;;
esac
