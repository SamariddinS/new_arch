---
title: RBAC
---

We integrate RBAC via custom dependencies that plug into FastAPI’s Depends system.

::: caution
Since fba v1.2.0, “role-menu” is the default RBAC strategy. Casbin is provided as an external plugin.
:::

## Role-Menu

Configure as follows to enable this mode.

::: steps

1. Add route dependencies

   Add the following dependencies to enable authorization for a route:

   ```py{5-6}
   @router.post(
       '',
       summary='xxx',
       dependencies=[
           Depends(RequestPermission('sys:api:add')),  # Usually xxx:xxx:xxx format
           DependsRBAC,
       ],
   )
   ```

2. Add permission codes in the system menu

   Values like `sys:api:add` correspond to menu permission codes. They must match and the user must own the menu to gain the operation permission.

:::

## Casbin

Casbin is a popular and flexible solution. You can define various control rules via models.

To use it, first get the plugin, then:

::: steps

1. Install the plugin

2. Enable authorization

   Set `RBAC_ROLE_MENU_MODE` to `False` in `backend/core/conf.py`.

:::

## Decoupling

In actual project development, it is not possible to have multiple RBAC solutions coexisting simultaneously. You can remove the Role Menu integration using the following methods:

- Remove the `RequestPermission` class and all class calls from the `backend/common/security/permission.py` file
- Remove `RBAC_ROLE_MENU_MODE` and `RBAC_ROLE_MENU_EXCLUDE` from the `backend/core/conf.py` file
- Remove the `if settings.RBAC_ROLE_MENU_MODE:` condition and related code from the `rbac_verify` method in `backend/common/security/rbac.py`
- Remove the `perms` column from the menu, along with its associated schema fields and SQL scripts
- Remove the button types from the `type` column in the menu, along with their related code logic and SQL scripts
