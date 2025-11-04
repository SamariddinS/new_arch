---
title: Timezone
---

We provide a unified timezone strategy. Change the global timezone by editing `backend/core/conf.py`.

::: caution
Once chosen, avoid changing timezones later to prevent persisted data inconsistencies.
:::

## Usage in code

Always use helpers in `backend/utils/timezone.py` instead of using datetime modules directly.

## Database

Handling timezones in DBs is tricky. Common approaches:

- Store/read UTC, convert on frontend (good for i18n)
- Store/read local tz, convert according to frontend tz (good for localization)
- Store numeric timestamps, convert on frontend (hard to manage, easy to operate)

An example:

::: chat title="Group chat"
{:2025-08-26 12:44:00}

{Wang}
Why do queries with different timezones/timestamps return the same data?

![question_db_timezone](/images/question_db_timezone.png)

Using MySQL, the two datetimes should have different timestamps, yet results look the same.

{Wang}
Raw SQL behaves as expected: first has rows, second none.

![question_sql_timezone](/images/question_sql_timezone.png)

Switching to PostgreSQL yields expected query results.

{.}
**timezone**: not used by the MySQL dialect.

SQLAlchemy and most Python MySQL drivers ignore MySQL timezone info, often discarding it, even for TIMESTAMP.

{.}
More specifically：[sqlalchemy/1985](https://github.com/sqlalchemy/sqlalchemy/issues/1985)
:::

We use the second approach and a custom TimeZone type in `backend/common/model.py`. Use your IDE to jump to its usages.
