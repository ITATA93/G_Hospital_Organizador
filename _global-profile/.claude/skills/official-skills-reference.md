# Claude Code Official Skills Reference

## Built-in Slash Commands

### /commit
Create a git commit with AI-generated message.
```
/commit
/commit -m "custom message"
```

### /pr
Create a pull request.
```
/pr
/pr --title "PR title" --body "description"
```

### /review
Review code changes.
```
/review           # Review uncommitted changes
/review HEAD~3    # Review last 3 commits
```

### /help
Get help with Claude Code.
```
/help
/help commands
```

### /clear
Clear conversation context.
```
/clear
```

### /compact
Compact conversation history.
```
/compact
```

### /init
Initialize Claude Code in a project.
```
/init
```

### /config
Manage configuration.
```
/config
/config set key value
```

## Custom Slash Commands Location
Place custom commands in:
- Project: `.claude/commands/{name}.md`
- Global: `~/.claude/commands/{name}.md`

## Command File Format
```markdown
Your prompt instructions here.

Variables available:
- {{input}} - User's additional input
- {{cwd}} - Current working directory
```

## MCP Servers
Claude Code supports MCP (Model Context Protocol) servers for extended capabilities:
- filesystem
- github
- postgres
- Custom servers

Configure in `.claude/settings.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"]
    }
  }
}
```
