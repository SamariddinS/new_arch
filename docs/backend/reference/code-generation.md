---
title: Code Generation
---

::: tip
This feature currently applies to the backend only, not the frontend.
:::

::: warning
API calls alone won’t preview generated code; use with the frontend. See Preview.
:::

## Concepts

Code generation consists of Business and Model modules.

### Business

Holds generator configuration. See `backend/app/generator/model/gen_business.py`.

### Model

Contains model column info required by the generator, similar to defining ORM models. Current capabilities are limited.

## Modes

Two modes: manual and automatic.

### Manual

::: tip
Use when defining tables/columns directly via the frontend.
:::

1. Use the business creation API to add a business entry
2. Use the model creation API to add model columns
3. Call `preview`, `generate` (write to disk), and `download`

### Automatic

::: tip
Use when tables/columns already exist in the database.
:::

1. Call `tables` to list DB tables
2. Call `import` to import tables; business and model columns are created automatically
3. Call `preview`, `generate` (write to disk), and `download`

## Preview

![cg1](/images/code-generator1.png)

![cg2](/images/code-generator2.png)
