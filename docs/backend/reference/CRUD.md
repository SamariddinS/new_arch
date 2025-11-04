---
title: CRUD
---

fba uses sqlalchemy-crud-plus as the base for DB operations. It’s our SQLAlchemy 2.0 based advanced async CRUD SDK, suitable for any FastAPI + SQLAlchemy project.

<LinkCard
title="sqlalchemy-crud-plus"
description="Advanced async CRUD SDK built on SQLAlchemy 2.0"
href="https://github.com/fastapi-practices/sqlalchemy-crud-plus"
icon="https://wu-clan.github.io/picx-images-hosting/logo/fba.png"
/>

## Function naming

fba follows these conventions:

- Fetch detail: `get()`
- Fetch detail by field: `get_by_xxx()`
- Build selectable: `get_select()`
- Fetch list: `get_list()`
- Fetch all: `get_all()`
- Children: `get_children()`
- With relations: `get_with_relation()`
- Create: `create()`
- Update: `update()`
- Delete: `delete()`
