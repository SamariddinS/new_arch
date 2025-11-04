---
title: Frequently Asked Questions
---

::: tip
If the following solutions don’t help, please contact us via the [community group](./group.md).
:::

## Response data doesn’t match the database

### Not the first deployment or redeployments

If the fba API has been called before, related data may have already been cached in Redis. Even after redeploying fba, the deployment will not automatically clear Redis caches.

So when you call the fba API after redeployment and see abnormal results while the database looks correct, it’s likely due to stale cache. Manually clear fba-related caches in Redis and the system will return to normal.

### Manual database changes

If you modify data directly in the database but the API response doesn’t change, the response may be served from Redis. Direct database edits do not trigger cache invalidation.

Manually clear the related keys in Redis to reflect the updated data in responses.

## Can't call await_only() here

```json
{
  "code": 500,
  "msg": "(sqlalchemy.exc.MissingGreenlet) greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place?\n[SQL: SELECT sys_dict_data.id AS sys_dict_data_id, sys_dict_data.label AS sys_dict_data_label, sys_dict_data.value AS sys_dict_data_value, sys_dict_data.sort AS sys_dict_data_sort, sys_dict_data.status AS sys_dict_data_status, sys_dict_data.remark AS sys_dict_data_remark, sys_dict_data.type_id AS sys_dict_data_type_id, sys_dict_data.created_time AS sys_dict_data_created_time, sys_dict_data.updated_time AS sys_dict_data_updated_time \nFROM sys_dict_data \nWHERE %s = sys_dict_data.type_id]\n[parameters: [{'%(2071788311008 param)s': 1}]]\n(Background on this error at: https://sqlalche.me/e/20/xd2s)",
  "data": null,
  "trace_id": "89afd9b0f2b8442590661701e2b6b495"
}
```

![await_only](/images/sqlalchemy_await_only.png)

In SQLAlchemy 2.0 async, relationships default to [lazy loading](https://docs.sqlalchemy.org/en/20/glossary.html#term-lazy-loading). If you don’t specify load strategies for related fields in your ORM query, those attributes may be in an error state (as shown above). When Pydantic/FastAPI tries to serialize them, it triggers an error because the field itself is invalid.

There are multiple solutions; see the SQLAlchemy docs. fba uses `noload()` by default to avoid this. For example:

```python
return await self.select_order(  # [!code word:noload]
   'id',
   'desc',
   load_options=[
       selectinload(self.model.dept).options(noload(Dept.parent), noload(Dept.children), noload(Dept.users)),
       selectinload(self.model.roles).options(noload(Role.users), noload(Role.menus), noload(Role.scopes)),
   ],
   **filters,
)
```

## PostgreSQL auto-increment primary key fails

If you insert rows via SQL scripts, PostgreSQL sequences might not sync with the max value in the table. Subsequent inserts from code can fail with `DETAIL: Key (id)=(x) already exists`.

Search for how to reset a PostgreSQL sequence to fix it.

## Database timezone pitfalls

MySQL doesn’t support timezone-aware column types, while PostgreSQL does. Storing timestamps correctly can be tricky. We provide a robust, cross‑DB solution compatible with both PostgreSQL and MySQL. See details: ./backend/reference/timezone.md
