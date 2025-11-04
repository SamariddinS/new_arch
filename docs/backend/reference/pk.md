---
title: Primary Key
---

fba supports two primary key strategies: traditional auto-increment ID and Snowflake ID. We use auto-increment as the global default declaration method.

Before switching, review their characteristics to decide if a change is necessary.

## Auto-increment ID

### Advantages

- Simple and easy to use
- Natively supported by databases
- Sequentially increasing
- High query performance
- Small storage footprint

### Limitations

- Possible ID conflicts in distributed systems; limited scalability
- Generation depends on the DB; potential bottleneck
- IDs are predictable, which may expose data volume or pose security risks

## Snowflake ID

### Advantages

- Friendly to distributed environments
- Globally unique without a central DB
- Timestamp-based and roughly ordered; good for sorting/querying

### Limitations

- More complex; requires generator maintenance
- Time rollback (clock drift) can block inserts
- Longer IDs; slightly higher storage/transfer cost

## When to use

### Auto-increment ID

Single-node or small/medium apps; simple business; no sensitivity to predictable IDs.

### Snowflake ID

Distributed systems, microservices, or high-concurrency, multi-region unique ID generation.

## Switching

### Auto-increment ID

No change needed; this is the fba default.

### Snowflake ID

1. Change all SQLAlchemy models from `id: Mapped[id_key]` to `id: Mapped[snowflake_id_key]`
2. Replace imports of `id_key` with `snowflake_id_key`
3. Run `backend/sql/init_snowflake_test_data.sql` to initialize test data

::: caution Windows notice
On Windows with MySQL >= 8.0, change `mysql+asyncmy` to `mysql+aiomysql` in `backend/database/db.py` to avoid insert failures. See issue asyncmy/issues/35.
:::

## Notes

- Ensure clock sync (e.g., NTP) and unique node IDs when using Snowflake
- Watch for conflicts when migrating/merging data with auto-increment IDs
- Frontend rendering of long integers may overflow

  When the API returns long integers, results are correct, but frontend rendering may corrupt them.

  You may see IDs differ after rendering. Best fix: serialize long ints to strings in responses.

  ::: tabs
  @tab schemaBase

  ```python
  @field_serializer('id', check_fields=False)
  def serialize_id(self, value) -> str:
      return str(value)
  ```

  @tab GetXxxDetail / GetXxxTree

  ```python
  @field_serializer('id')
  def serialize_id(self, value) -> str:
      return str(value)
  ```





