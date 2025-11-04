---
title: Router
---

Routers in fba follow the Restful API specification

## Router Structure

We have a historical discussion about routers. If you're interested, you can check it out: [#4](https://github.com/fastapi-practices/fastapi_best_architecture/discussions/4)

The current router structure is as follows:

::: file-tree

- backend Backend
    - app Application
        - xxx Custom application <Badge type="warning" text="Contains subpackages" />
            - api API
                - v1
                    - xxx Subpackage
                        - __init__.py Register routers from xxx.py files in the subpackage in this file
                        - xxx.py
                        - ...
                - __init__.py
                - router.py Register all routers from subpackage __init__.py files in this file
        - xxx Custom application <Badge type="warning" text="No subpackages" />
            - api API
                - v1
                    - __init__.py No operations needed
                    - xxx.py
                    - ...
                - __init__.py
                - router.py Register all routers from xxx.py files in this file
    - __init__.py
    - router.py Register all routers from router.py files in the app directory in this file

:::

::: warning
We have uniformly named all API router parameters as router, which is very helpful for writing APIs. However, we cannot ignore that when registering routers, we must pay attention to our import method.

In fba, we can view all router imports. They look like `from backend.app.admin.api.v1.sys.api import router as api_router`.
We must import the router parameter `router` from the file here. To avoid parameter name conflicts, we can use `as` to create an alias for the router parameter.
:::
