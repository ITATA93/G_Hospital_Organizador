#!/bin/bash
#
# disable.sh - Disable an agent or skill for a specific vendor
#
# Usage:
#   ./disable.sh agent <name> <vendor>
#   ./disable.sh skill <name> <vendor>
#
# Examples:
#   ./disable.sh agent researcher codex
#   ./disable.sh skill skill-creator codex
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

success() { echo -e "${GREEN}[OK]${NC} $1"; }
warning() { echo -e "${YELLOW}[!!]${NC} $1"; }
error() { echo -e "${RED}[XX]${NC} $1"; exit 1; }

# Validate arguments
if [ $# -lt 3 ]; then
    echo "Usage: $0 <agent|skill> <name> <vendor>"
    echo ""
    echo "Vendors: gemini, claude, codex"
    echo ""
    echo "Examples:"
    echo "  $0 agent researcher codex"
    echo "  $0 skill skill-creator codex"
    exit 1
fi

TYPE="$1"
NAME="$2"
VENDOR="$3"

# Validate type
if [ "$TYPE" != "agent" ] && [ "$TYPE" != "skill" ]; then
    error "Type must be 'agent' or 'skill'"
fi

# Validate vendor
case "$VENDOR" in
    gemini|claude|codex) ;;
    *) error "Vendor must be: gemini, claude, or codex" ;;
esac

# Set target path based on vendor and type
case "$VENDOR" in
    gemini)
        if [ "$TYPE" = "agent" ]; then
            TARGET_DIR="$HOME/.gemini/agents"
        else
            TARGET_DIR="$HOME/.gemini/skills"
        fi
        ;;
    claude)
        if [ "$TYPE" = "agent" ]; then
            TARGET_DIR="$HOME/.claude/agents"
        else
            TARGET_DIR="$HOME/.claude/skills"
        fi
        ;;
    codex)
        if [ "$TYPE" = "agent" ]; then
            TARGET_DIR="$HOME/.codex/agents"
        else
            TARGET_DIR="$HOME/.codex/skills"
        fi
        ;;
esac

TARGET_FILE="$TARGET_DIR/${NAME}.md"

# Check if exists
if [ ! -e "$TARGET_FILE" ]; then
    warning "Not enabled (file not found): $TARGET_FILE"
    exit 0
fi

# Check if it's a symlink
if [ -L "$TARGET_FILE" ]; then
    rm "$TARGET_FILE"
    success "Disabled $TYPE '$NAME' for $VENDOR"
    echo "  Removed symlink: $TARGET_FILE"
else
    warning "File exists but is not a symlink. Not removing."
    echo "  To force remove: rm \"$TARGET_FILE\""
    exit 1
fi
