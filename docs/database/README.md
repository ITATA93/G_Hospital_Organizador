# Database Documentation

This directory contains database-related documentation for the project.

## Contents

- `schema.md` - Database schema documentation
- `migrations/` - Migration history and notes
- `queries/` - Common queries and performance notes
- `erd.md` - Entity Relationship Diagrams

## Schema Documentation Template

When documenting tables, use this format:

```markdown
## Table: table_name

**Purpose:** Brief description

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary identifier |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |

**Indexes:**
- `idx_table_column` on (column)

**Relations:**
- FK to `other_table(id)`
```

## Migration Naming Convention

```
YYYYMMDD_HHMMSS_description.sql
```

Example: `20240201_143022_add_users_table.sql`

## Best Practices

1. **Always document schema changes** before applying migrations
2. **Include rollback scripts** for each migration
3. **Document query performance** for complex queries
4. **Keep ERD updated** when schema changes
