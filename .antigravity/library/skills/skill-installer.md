---
name: skill-installer
description: Install Codex skills from GitHub repositories, local files, or URLs. Use this when adding new skills to the Codex environment.
---

# Skill Installer

## Overview

This skill helps install Codex skills from various sources including GitHub repositories, local files, and raw URLs. It handles downloading, validating, and placing skills in the correct directory.

## When to Use

Use this skill when:
- Installing skills from GitHub
- Copying skills from another project
- Downloading shared skills from URLs
- Setting up skills on a new machine

## Installation Sources

### 1. GitHub Repository
```bash
# Full repo with skills directory
git clone https://github.com/user/repo ~/.codex/skills/repo-name

# Specific skill file
curl -o ~/.codex/skills/skill-name.md \
  https://raw.githubusercontent.com/user/repo/main/skills/skill-name.md
```

### 2. Local File
```bash
# Copy single skill
cp /path/to/skill.md ~/.codex/skills/

# Copy skill directory
cp -r /path/to/skill-dir ~/.codex/skills/
```

### 3. URL
```bash
curl -o ~/.codex/skills/skill-name.md https://example.com/skill.md
```

## Installation Workflow

### Step 1: Identify Source
Ask the user for:
- Source type (GitHub, local, URL)
- Repository/path/URL
- Specific skill name if partial install

### Step 2: Validate Source
Check that the source:
- Is accessible (network/permissions)
- Contains valid skill files (.md with frontmatter)
- Doesn't conflict with existing skills

### Step 3: Install

#### From GitHub Repository
```bash
# Clone entire skills repo
REPO="https://github.com/user/codex-skills"
TARGET_DIR="$HOME/.codex/skills"

git clone --depth 1 "$REPO" /tmp/codex-skills-temp
cp -r /tmp/codex-skills-temp/skills/* "$TARGET_DIR/"
rm -rf /tmp/codex-skills-temp

# Or clone to named directory
git clone --depth 1 "$REPO" "$TARGET_DIR/skill-collection"
```

#### From Specific File URL
```bash
SKILL_URL="https://raw.githubusercontent.com/user/repo/main/skill.md"
SKILL_NAME="skill-name.md"

curl -fsSL "$SKILL_URL" -o "$HOME/.codex/skills/$SKILL_NAME"
```

#### From Local Path
```bash
# File
cp /path/to/source/skill.md ~/.codex/skills/

# Directory (preserves structure)
cp -r /path/to/source/skill-dir ~/.codex/skills/
```

### Step 4: Verify Installation
```bash
# Check file exists
ls -la ~/.codex/skills/skill-name.md

# Validate frontmatter
head -10 ~/.codex/skills/skill-name.md
```

### Step 5: Test Skill
```bash
codex exec "Use the {skill-name} skill to {example task}"
```

## Popular Skill Sources

| Source | URL | Description |
|--------|-----|-------------|
| OpenAI Official | github.com/openai/codex | Core Codex skills |
| Community | github.com/topics/codex-skills | Community-contributed |
| Antigravity | This workspace | Multi-vendor skills |

## Validation Checks

Before installing, verify:

1. **Frontmatter exists**
   ```yaml
   ---
   name: skill-name
   description: ...
   ---
   ```

2. **No conflicting names**
   ```bash
   ls ~/.codex/skills/ | grep skill-name
   ```

3. **File permissions**
   ```bash
   chmod 644 ~/.codex/skills/skill-name.md
   ```

## Troubleshooting

### Skill not recognized
- Verify file has `.md` extension
- Check frontmatter has `name` field
- Restart Codex session

### Permission denied
```bash
# Fix permissions
chmod -R u+rw ~/.codex/skills/
```

### Conflicts with existing skill
```bash
# Backup and replace
mv ~/.codex/skills/skill-name.md ~/.codex/skills/skill-name.md.bak
# Then install new version
```

## Bulk Installation

For multiple skills:
```bash
# From text file with URLs
while read -r url; do
  name=$(basename "$url")
  curl -fsSL "$url" -o "$HOME/.codex/skills/$name"
done < skill-urls.txt

# From GitHub directory listing
gh api repos/user/repo/contents/skills | \
  jq -r '.[].download_url' | \
  while read -r url; do
    name=$(basename "$url")
    curl -fsSL "$url" -o "$HOME/.codex/skills/$name"
  done
```

## Uninstalling Skills

```bash
# Remove single skill
rm ~/.codex/skills/skill-name.md

# Remove skill directory
rm -rf ~/.codex/skills/skill-dir/

# List all installed skills
ls ~/.codex/skills/
```

## Output

After installation, report:
1. Installed skill name(s)
2. Installation path
3. Verification status
4. Test command to run
