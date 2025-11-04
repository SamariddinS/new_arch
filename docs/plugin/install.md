---
title: Plugin Installation
---

::: caution
Do not install plugins directly in production to avoid unnecessary risk.
:::

## Backend

:::: tabs
@tab Manual

1. Download the plugin repository source
2. Copy the plugin folder into `backend/plugin`
3. Configure per the plugin’s README.md
4. Restart the service

@tab ZIP

1. Obtain a packaged plugin ZIP <Badge type="warning" text="either" />

    - Download the repository as a ZIP

      ::: details GitHub Example
      ![zip](/images/plugin_zip.png)
      :::

    - Or use fba’s plugin download API to get the ZIP

2. Install via fba’s ZIP install API
3. Configure per README.md
4. Restart the service

@tab GIT

1. Get the plugin Git URL (GitHub, GitLab, Gitee, Gitea, ...)
2. Install via fba’s Git install API
3. Configure per README.md
4. Restart the service

@tab CLI

1. Run `fba add -h` for help
2. Install via `fba add`
3. Configure per README.md
4. Restart the service

::::

::: warning
After installing a plugin, before restarting fba, ensure the SQLAlchemy models (if any) use the same primary key strategy as your app. See: ../backend/reference/pk.md
:::

## Frontend

1. Download the plugin repository source
2. Copy the folder into `apps/web-antd/src/plugins`
3. Restart the service
