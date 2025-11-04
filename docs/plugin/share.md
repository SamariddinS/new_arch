---
title: Share Your Plugin
---

## Backend

:::: steps

1. Create a plugin repository

   Use the template repo: fba_plugin_template

   ::: warning Naming rule
   `repo name == plugin name`

   If your repo is `sms`, installing it creates `backend/plugin/sms`.

   Plugin names must be unique; avoid collisions.
   :::

   ![repo](/images/plugin_template.png)

2. Push code

   Copy all developed plugin files from fba into your repository.

   ::: caution
   Copy contents of the plugin folder, not the folder itself.
   :::

::::

## Frontend

:::: steps

1. Create a plugin repository

   Use the template repo: fba_ui_plugin_template

   ::: warning Naming rule
   `repo name == <plugin>_ui`

   If your repo is `sms_ui`, installing it creates `apps/web-antd/src/plugins/sms`.

   Plugin names must be unique; avoid collisions.
   :::

2. Push code

   Copy all plugin files developed in fba_ui (Vben Admin Antd only).

   ::: caution
   Copy contents of the plugin folder, not the folder itself.
   :::

::::

## Publish

We provide a simple [Plugin Market](../market.md) for showcasing and navigation.

If your plugin is compatible with fba, please share it in the Discord community channel: Plugin System.
