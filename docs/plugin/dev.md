---
title: Plugin Development
---

::: info
The official repo includes several built-in plugins under `backend/plugin`. Reading this doc alongside the repo helps.
:::

## Backend

::: steps

1. Pull the latest fba and set up the dev environment
2. Learn how the plugin system works: types, routes, config, DB compatibility
3. Develop using the directory structure below
4. Finish development
5. Optionally: [share your plugin](./share.md)

:::

### Plugin types

::: tabs#plugin
@tab <Icon name="carbon:app" /> Application-level
Top-level folders under `app` are treated as applications; plugins of this type are injected like apps.

@tab <Icon name="fluent:table-simple-include-16-regular" /> Extension-level
Injected into existing applications under `app`.
:::

### Plugin routes

If a plugin meets the requirements, all its routes are auto-registered in FastAPI. Note startup time grows with the number of plugins because fba parses them at startup.

::: tabs#plugin
@tab <Icon name="carbon:app" /> Application-level
Follow the route structure documented at ../backend/reference/router.md #Routing Structure

@tab <Icon name="fluent:table-simple-include-16-regular" /> Extension-level
Mirror the target app’s `api` directory structure 1:1. See built-in plugin `notice` as reference.
:::

### Plugin config

Each plugin must include `plugin.toml`.

::: tabs#plugin
@tab <Icon name="carbon:app" /> Application-level

```toml
# Plugin info
[plugin]
# Summary (short description)
summary = ''
# Version
version = ''
# Description
description = ''
# Author
author = ''

# App config
[app]
# Final router instance (see backend/app/admin/api/router.py; usually named v1)
router = ['v1']
```

@tab <Icon name="fluent:table-simple-include-16-regular" /> Extension-level

```toml
# Plugin info
[plugin]
# Abstract (Brief Description)
summary = ''
# Version Number
version = ''
# Description
description = ''
# Author
author = ''

# App config
[app]
# Which app to extend
extend = 'app_folder_name'

# API config
[api.xxx]
# xxx is the filename (without suffix) under plugin api directory
# e.g. `notice.py` -> section name `notice`; repeat for multiple files
# Route prefix starting with '/'
prefix = ''
# Swagger tags
tags = ''
```

:::

### Database compatibility

Official implementations support both MySQL and PostgreSQL. Third-party plugins are not required to. See SQLAlchemy docs: TypeDecorator, with_variant.

### Directory structure

Place plugins under `backend/plugin`. Example structure:

::: file-tree

- xxx plugin name <Badge type="danger" text="required" />
    - api/ endpoints <Badge type="danger" text="required" />
    - crud/
    - model/
        - __init__.py import all models here <Badge type="danger" text="if present" />
    - schema/
    - service/
    - sql (optional SQL init)
        - mysql: init.sql
        - postgresql: init.sql
    - utils/
    - __init__.py keep as a package <Badge type="danger" text="required" />
    - plugin.toml config <Badge type="danger" text="required" />
    - README.md usage and contact <Badge type="danger" text="required" />
    - requirements.txt dependencies

:::

## Frontend

::: steps

1. Pull latest fba_ui and set up dev environment
2. Develop following the structure below
3. Finish development
4. Optionally: [share your plugin](./share.md)

:::

### Directory structure

Place plugins under `apps/web-antd/src/plugins`. Example:

::: file-tree

- xxx plugin name
    - api
        - index.ts
    - langs i18n
        - en-US
            - <plugin>.json
        - ru-RU
            - <plugin>.json
    - routes
        - index.ts
    - views
        - index.vue
        - …
    - … more content

:::

## Notes

Avoid referencing internal framework functions unless necessary; changes in the framework may break plugins that depend on them.
