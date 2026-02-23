# Database Documentation

## Overview

This document describes the database schema and configuration for the Antigravity Workspace.

## Configuration

Database connection is configured via environment variables:

```env
DATABASE_URL=sqlite:///./data/app.db
```

Supported databases:
- SQLite (default, for development)
- PostgreSQL (recommended for production)
- MySQL/MariaDB

---

## Schema

### Tables

#### `agents` (Future)

Stores agent configurations.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(100) | Agent name (unique) |
| description | TEXT | Agent description |
| category | VARCHAR(50) | Agent category |
| config | JSONB | Agent configuration |
| is_active | BOOLEAN | Whether agent is active |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

#### `executions` (Future)

Stores agent execution history.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| agent_id | UUID | Reference to agent |
| input | TEXT | Execution input |
| output | TEXT | Execution output |
| metadata | JSONB | Execution metadata |
| status | VARCHAR(20) | completed/failed/pending |
| duration_ms | INTEGER | Execution duration |
| created_at | TIMESTAMP | Execution timestamp |

---

## Migrations

Migrations are managed using Alembic (when implemented):

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Data Dictionary

### Agent Categories

| Value | Description |
|-------|-------------|
| analysis | Code analysis agents |
| documentation | Documentation generators |
| testing | Test generation agents |
| review | Code review agents |
| deployment | Deployment automation |

### Execution Status

| Value | Description |
|-------|-------------|
| pending | Waiting to execute |
| running | Currently executing |
| completed | Successfully completed |
| failed | Execution failed |

---

## Backup & Recovery

### SQLite
```bash
# Backup
cp data/app.db data/app.db.backup

# Restore
cp data/app.db.backup data/app.db
```

### PostgreSQL
```bash
# Backup
pg_dump -h localhost -U user dbname > backup.sql

# Restore
psql -h localhost -U user dbname < backup.sql
```
