---
title: Quick Start
---

::: caution
FBA targets experienced Python backend engineers. If you’re newer, start with the Slim Edition: ../summary/fsm.md
:::

## Local Development

:::: steps

1. Prepare local environment

    - Python 3.10+
    - PostgreSQL 16.0+ or MySQL 8.0+
      Snowflake ID users: see ../reference/pk.md {.read-more}
      MySQL users: see ../reference/db.md {.read-more}
    - Redis (latest stable recommended)

2. Create database: `fba`
    - PostgreSQL: create normally
    - MySQL: create with utf8mb4 charset

3. Start Redis
4. Get the source <Badge type="warning" text="Choose one" />

   ::: tabs
   @tab Clone source

   ```shell:no-line-numbers
   git clone https://github.com/fastapi-practices/fastapi_best_architecture.git
   ```

   @tab Create from template

   This project supports “Use this template” to create a non-fork repository. Click the button on GitHub, then `git clone` your new repo.

   ![use_this_template](/images/use_this_template.png)
   :::

5. Install dependencies

   We use `uv` as the project manager. Install: https://docs.astral.sh/uv/getting-started/installation/

   If `uv` is already installed, run `uv self update`.

   ::: code-tabs
   @tab <Icon name="material-icon-theme:uv" />uv - sync

   ```shell:no-line-numbers
   uv sync
   ```

   @tab <Icon name="material-icon-theme:uv" />uv - pip

   ```shell:no-line-numbers
   uv pip install -r requirements.txt
   ```
   :::

6. env

   From the `backend` dir, create a local env file:

   ```shell:no-line-numbers
   cp .env.example .env
   ```

7. Adjust configs as needed: `backend/core/conf.py` and `.env`
8. Create database tables <Badge type="warning" text="Choose one" />

   ::: tabs
   @tab Auto-create
   Skip this. FBA will auto-create after starting.

   @tab Alembic migrations
   From the `backend` dir:

   Generate migration:

   ```shell:no-line-numbers
   alembic revision --autogenerate
   ```

   Apply migration:

   ```shell:no-line-numbers
   alembic upgrade head
   ```
   :::

9. Run

   From the repo root, start the FastAPI app:

   ```shell:no-line-numbers
   fba run
   ```

10. Start Celery worker/beat/flower <Badge type="warning" text="Optional" />

    From the repo root, start Celery services:

    ::: code-tabs
    @tab Worker

     ```shell:no-line-numbers
     fba celery worker
     ```

    @tab Beat

     ```shell:no-line-numbers
     fba celery beat
     ```

    @tab Flower

     ```shell:no-line-numbers
     fba celery flower
     ```
    :::

    ::: warning
    If you never started these, task result tables won’t exist. Any API touching task results will error until worker and beat run at least once.
    :::

11. Seed test data

    Core: run scripts under `backend/sql/` for your PK mode.

    Plugins: run scripts under `plugin/sql/` for your PK mode.

    ::: info
    You can also use the CLI to run these quickly: ../reference/cli.md
    :::

12. Open: http://127.0.0.1:8000/docs

::::

## Development Flow

::: note
For reference only; follow your team’s habits.
:::

::: steps

1. Define database models: ../reference/model.md
2. Define validation schemas: ../reference/schema.md
3. Define routes: ../reference/router.md

4. Developing（service）

5. Writing database operations（[crud](../reference/CRUD.md)）

:::

## Unit Testing

::: info
Run unit tests using `pytest`. The project only provides a very basic demo and does not include a complete set of unit tests. If needed, please write your own.
:::

::: steps

1. Create the test database `fba_test` with utf8mb4 encoding. PostgreSQL users may omit the encoding specification.
2. Create database tables: Use the tool to generate DDL scripts for all tables in the `fba` database, then execute them in the `fba_test` database
3. Initialize test data: Use scripts matching the primary key schema in the `backend/sql/` directory to populate test data
4. Open a terminal in the project root directory and execute the following unit test commands

   ```shell:no-line-numbers
   pytest -vs --disable-warnings
   ```

:::
