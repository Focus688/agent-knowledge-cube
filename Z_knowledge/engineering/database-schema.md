# Z: Database Conventions

## Naming Conventions
- **Tables**: `snake_case`, plural: `users`, `order_items`, `product_reviews`
- **Columns**: `snake_case`, descriptive: `created_at`, `is_active`, `first_name`
- **Indexes**: `idx_{table}_{column}` — `idx_users_email`
- **Unique constraints**: `uq_{table}_{column}` — `uq_users_email`
- **Foreign keys**: `fk_{child_table}_{parent_table}` — `fk_order_items_orders`
- **Primary keys**: `id` (bigint auto-increment or UUID v4)

## Migration Policy
- One migration per change (no combining unrelated schema changes)
- File format: `YYYYMMDDHHMMSS_description.sql` (timestamp-prefixed)
- Every migration must have both `up` and `down` scripts
- Never modify a committed migration — create a new one
- Zero-downtime migrations: use `pt-online-schema-change` for large tables
- Migration review: required in PR for any schema change

## Indexing Strategy
- **Primary key**: always indexed (auto)
- **Foreign keys**: always index — prevents lock contention on joins
- **Filter columns**: index columns used in `WHERE`, `JOIN`, `ORDER BY`
- **Composite indexes**: order by selectivity (most selective first)
- **Covering indexes**: include all columns needed by the query
- **Avoid over-indexing**: max 5-7 indexes per table; monitor write perf
- Monitor unused indexes: `pg_stat_user_indexes` (PostgreSQL)

## Query Optimization
- Always `EXPLAIN ANALYZE` before deploying new queries
- Avoid `SELECT *` — select only needed columns
- Use `LIMIT` on all list queries (prevent full table scans)
- Batch inserts: `INSERT INTO ... VALUES (...), (...), (...);`
- Avoid N+1: use `JOIN` or batch loading (GraphQL DataLoader)
- Connection pooling: PgBouncer (max 50-100 connections per instance)

## Connection Pooling
- Application-side: max 10-20 connections per instance
- PgBouncer: transaction-level pooling mode
- Pool limits based on: `max_connections / (instances * pool_per_instance)`
- Monitor: `pg_stat_activity` for idle-in-transaction connections
