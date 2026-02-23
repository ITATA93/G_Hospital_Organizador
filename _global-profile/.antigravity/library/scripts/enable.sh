#!/bin/bash
#
# enable.sh - Enable an agent or skill for a specific vendor
#
# Usage:
#   ./enable.sh agent <name> <vendor>
#   ./enable.sh skill <name> <vendor>
#
# Examples:
#   ./enable.sh agent researcher codex
#   ./enable.sh skill skill-creator codex
#   ./enable.sh agent code-analyst gemini
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_DIR="$(dirname "$SCRIPT_DIR")"

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

# Set paths based on type
if [ "$TYPE" = "agent" ]; then
    SOURCE_DIR="$LIBRARY_DIR/agents"
    SOURCE_FILE="$SOURCE_DIR/${NAME}.md"
else
    SOURCE_DIR="$LIBRARY_DIR/skills"
    SOURCE_FILE="$SOURCE_DIR/${NAME}.md"
fi

# Check source exists
if [ ! -f "$SOURCE_FILE" ]; then
    error "Source file not found: $SOURCE_FILE"
fi

# Set target path based on vendor
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

# Create target directory if not exists
mkdir -p "$TARGET_DIR"

# Check if already enabled
if [ -e "$TARGET_FILE" ]; then
    if [ -L "$TARGET_FILE" ]; then
        warning "Already enabled (symlink exists): $TARGET_FILE"
        exit 0
    else
        warning "File exists but is not a symlink. Backing up..."
        mv "$TARGET_FILE" "${TARGET_FILE}.backup"
    fi
fi

# Create symlink
ln -s "$SOURCE_FILE" "$TARGET_FILE"
success "Enabled $TYPE '$NAME' for $VENDOR"
echo "  Source: $SOURCE_FILE"
echo "  Target: $TARGET_FILE"
