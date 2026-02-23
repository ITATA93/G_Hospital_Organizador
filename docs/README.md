# Documentation — Antigravity Workspace

This directory contains all project documentation.

## Structure

```
docs/
├── README.md           ← This file
├── TODO.md             ← Prioritized pending tasks
├── DEVLOG.md           ← Development diary
├── architecture/       ← System architecture and design decisions
│   └── ARCHITECTURE.md
├── api/                ← API documentation
├── database/           ← Database schemas and queries
├── decisions/          ← Architecture Decision Records (ADRs)
└── research/           ← Deep research outputs
```

## Key Documents

| Document | Purpose |
|----------|---------|
| [TODO.md](TODO.md) | Track pending tasks with priorities |
| [DEVLOG.md](DEVLOG.md) | Daily development log |
| [ARCHITECTURE.md](architecture/ARCHITECTURE.md) | System design overview |

## Maintenance

- **doc-writer** sub-agent maintains these files
- Update DEVLOG.md at end of each session
- Keep TODO.md prioritized and current
- Document architectural decisions in decisions/
