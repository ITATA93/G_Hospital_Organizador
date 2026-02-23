#!/bin/bash
#
# install-global.sh
# Installs Antigravity global profile to user's home directory.
#
# Usage:
#   ./install-global.sh [options]
#
# Options:
#   -f, --force    Overwrite existing configuration
#   -b, --backup   Create backup before overwriting (requires -f)
#
# Examples:
#   ./install-global.sh
#   ./install-global.sh --force
#   ./install-global.sh --force --backup
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

success() { echo -e "${GREEN}[OK]${NC} $1"; }
warning() { echo -e "${YELLOW}[!!]${NC} $1"; }
info() { echo -e "${CYAN}[..]${NC} $1"; }
error() { echo -e "${RED}[XX]${NC} $1"; }

# Parse arguments
FORCE=false
BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--force)
            FORCE=true
            shift
            ;;
        -b|--backup)
            BACKUP=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo ""
echo -e "${MAGENTA}=============================================${NC}"
echo -e "${MAGENTA}  ANTIGRAVITY GLOBAL PROFILE INSTALLER${NC}"
echo -e "${MAGENTA}=============================================${NC}"
echo ""

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_GEMINI="$SCRIPT_DIR/.gemini"
SOURCE_CLAUDE="$SCRIPT_DIR/.claude"
SOURCE_CODEX="$SCRIPT_DIR/.codex"

HOME_DIR="$HOME"
TARGET_GEMINI="$HOME_DIR/.gemini"
TARGET_CLAUDE="$HOME_DIR/.claude"
TARGET_CODEX="$HOME_DIR/.codex"

info "Source: $SCRIPT_DIR"
info "Target: $HOME_DIR"

# Check source exists
if [ ! -d "$SOURCE_GEMINI" ]; then
    error "Source .gemini directory not found: $SOURCE_GEMINI"
    exit 1
fi

# ============================================
# PHASE 1: Handle existing configuration
# ============================================
echo ""
echo -e "${YELLOW}--- Phase 1: Checking existing configuration ---${NC}"

GEMINI_EXISTS=false
CLAUDE_EXISTS=false
CODEX_EXISTS=false

[ -d "$TARGET_GEMINI" ] && GEMINI_EXISTS=true
[ -d "$TARGET_CLAUDE" ] && CLAUDE_EXISTS=true
[ -d "$TARGET_CODEX" ] && CODEX_EXISTS=true

if [ "$GEMINI_EXISTS" = true ] || [ "$CLAUDE_EXISTS" = true ] || [ "$CODEX_EXISTS" = true ]; then
    if [ "$FORCE" = false ]; then
        warning "Existing configuration found:"
        [ "$GEMINI_EXISTS" = true ] && warning "  - $TARGET_GEMINI"
        [ "$CLAUDE_EXISTS" = true ] && warning "  - $TARGET_CLAUDE"
        [ "$CODEX_EXISTS" = true ] && warning "  - $TARGET_CODEX"
        error "Use --force to overwrite or --force --backup to backup first"
        exit 1
    fi

    if [ "$BACKUP" = true ]; then
        TIMESTAMP=$(date +%Y%m%d-%H%M%S)

        if [ "$GEMINI_EXISTS" = true ]; then
            BACKUP_GEMINI="$TARGET_GEMINI.backup-$TIMESTAMP"
            mv "$TARGET_GEMINI" "$BACKUP_GEMINI"
            success "Backed up: $BACKUP_GEMINI"
        fi

        if [ "$CLAUDE_EXISTS" = true ]; then
            BACKUP_CLAUDE="$TARGET_CLAUDE.backup-$TIMESTAMP"
            mv "$TARGET_CLAUDE" "$BACKUP_CLAUDE"
            success "Backed up: $BACKUP_CLAUDE"
        fi

        if [ "$CODEX_EXISTS" = true ]; then
            BACKUP_CODEX="$TARGET_CODEX.backup-$TIMESTAMP"
            mv "$TARGET_CODEX" "$BACKUP_CODEX"
            success "Backed up: $BACKUP_CODEX"
        fi
    else
        [ "$GEMINI_EXISTS" = true ] && rm -rf "$TARGET_GEMINI" && warning "Removed existing: $TARGET_GEMINI"
        [ "$CLAUDE_EXISTS" = true ] && rm -rf "$TARGET_CLAUDE" && warning "Removed existing: $TARGET_CLAUDE"
        [ "$CODEX_EXISTS" = true ] && rm -rf "$TARGET_CODEX" && warning "Removed existing: $TARGET_CODEX"
    fi
fi

# ============================================
# PHASE 2: Copy configuration
# ============================================
echo ""
echo -e "${YELLOW}--- Phase 2: Installing configuration ---${NC}"

# Copy .gemini
cp -r "$SOURCE_GEMINI" "$TARGET_GEMINI"
success "Installed: ~/.gemini/"

# Copy .claude if exists
if [ -d "$SOURCE_CLAUDE" ]; then
    cp -r "$SOURCE_CLAUDE" "$TARGET_CLAUDE"
    success "Installed: ~/.claude/"
fi

# Copy .codex if exists
if [ -d "$SOURCE_CODEX" ]; then
    cp -r "$SOURCE_CODEX" "$TARGET_CODEX"
    success "Installed: ~/.codex/"
fi

# Copy GEMINI.md to home if it doesn't exist
SOURCE_GEMINI_MD="$SCRIPT_DIR/GEMINI.md"
TARGET_GEMINI_MD="$HOME_DIR/GEMINI.md"
if [ -f "$SOURCE_GEMINI_MD" ] && [ ! -f "$TARGET_GEMINI_MD" ]; then
    cp "$SOURCE_GEMINI_MD" "$TARGET_GEMINI_MD"
    success "Installed: ~/GEMINI.md"
fi

# ============================================
# PHASE 3: Verify installation
# ============================================
echo ""
echo -e "${YELLOW}--- Phase 3: Verifying installation ---${NC}"

ALL_OK=true

check_path() {
    if [ -e "$1" ]; then
        success "Found: $2"
    else
        warning "Missing: $2"
        ALL_OK=false
    fi
}

check_path "$TARGET_GEMINI/settings.json" "settings.json"
check_path "$TARGET_GEMINI/agents" "agents/"
check_path "$TARGET_GEMINI/commands" "commands/"
check_path "$TARGET_GEMINI/rules" "rules/"

# ============================================
# SUMMARY
# ============================================
echo ""
if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}=============================================${NC}"
    echo -e "${GREEN}  INSTALLATION COMPLETE!${NC}"
    echo -e "${GREEN}=============================================${NC}"
else
    echo -e "${YELLOW}=============================================${NC}"
    echo -e "${YELLOW}  INSTALLATION COMPLETE (with warnings)${NC}"
    echo -e "${YELLOW}=============================================${NC}"
fi
echo ""
echo -e "${CYAN}Installed to:${NC}"
echo "  ~/.gemini/     - Gemini CLI configuration"
echo "  ~/.claude/     - Claude Code configuration"
echo "  ~/.codex/      - Codex CLI configuration"
echo ""
echo -e "${YELLOW}Test with:${NC}"
echo "  gemini 'Hello, test the configuration'"
echo "  gemini -e code-analyst 'List available agents'"
echo "  codex exec 'Hello, test Codex configuration'"
echo ""
