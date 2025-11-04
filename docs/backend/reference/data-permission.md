---
title: Data Permissions
---

Data permissions are established to add access controls to data. The most common implementation approach involves restricting data to "own data only", "department data only", etc.
These are what we call data permissions. You can control different roles to have different data permissions, achieving isolation between users and data.

## Common Approach

::: caution
fba has removed this integration method. This code is retained only as an example.
:::

@[code python](../../code/data_perm.py)

### Drawbacks

This common data permission approach can satisfy most daily scenarios. However, it has serious limitations. Since data filtering is implemented through
SQL statement concatenation, these fixed permissions hardcode data permission requirements.

For example: business tables must contain dept_id and created_by fields. If a business table lacks these fields, you cannot control data permissions via SQL.

## Built-in Solution

Is there a more flexible approach? The answer is yes. Currently, fba implements an ultra-flexible solution, though configuration is more complex compared to the common approach.

You can view the source code directly at `backend/common/security/permission.py`.
It implements data filtering using a nearly identical approach to the conventional method, but due to its complexity, we'll explain it through this video: [Data Permission Management](https://www.bilibili.com/video/BV13hioY1EQU/?share_source=copy_web\&vd_source=ccb2aae47e179a51460c20d165021cb7)
