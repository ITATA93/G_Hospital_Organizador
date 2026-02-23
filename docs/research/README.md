# Research Archive

This directory stores research findings from the `researcher` agent.

## File Naming Convention
```
YYYY-MM-DD_<topic-slug>.md
```

## Example
```
2026-02-02_oauth-best-practices.md
2026-02-02_react-server-components.md
```

## Usage
```bash
# Via dispatcher
./.subagents/dispatch.sh researcher "Research OAuth 2.1 best practices"

# Via Codex direct
codex exec --deep-research "Research topic"
```

Research files include:
- Executive summary
- Key findings with citations
- Actionable recommendations
- Source table with URLs and access dates
