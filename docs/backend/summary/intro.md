---
title: Introduction
---

An enterprise-grade backend architecture solution built on FastAPI.

## Quasi Three-Layer Architecture

MVC is a common design pattern in Python web apps, but a three-layered architecture is often more appealing.

There is no universal standard for a three-layer architecture in Python web development, so we call it a “quasi three-layer architecture”.

! Please note!

We do not follow the traditional multi-app (microservice) layout (Django, SpringBoot, ...). Instead, we use an opinionated layout (see Project Structure).

If you don’t like this style, feel free to adapt it.

| Module   | java           | fastapi_best_architecture |
|------|----------------|---------------------------|
| View   | controller     | api                       |
| Data Transmission | dto            | schema                    |
| Business Logic | service + impl | service                   |
| Data Access | dao / mapper   | crud                      |
| Model   | entity         | model                     |

## Features

- [x] Global FastAPI PEP 593 Annotated parameter style
- [x] Full async/await with asgiref-based design
- [x] RESTful API conventions
- [x] SQLAlchemy 2.0 new ORM syntax
- [x] Pydantic v2
- [x] Role-menu RBAC access control
- [x] Celery for async tasks
- [x] In-house JWT authentication middleware
- [x] Global custom timezone support
- [x] Docker / Docker Compose deployment
- [x] Pytest integration

## Built-in Modules

- [x] User management: assign roles and permissions
- [x] Department management: organizational structure (company, dept, group)
- [x] Menu management: menu and button-level permissions
- [x] Role management: configure roles, assign menus and permissions
- [x] Dict management: common parameters and configs
- [x] Parameter management: dynamic system parameters
- [x] Announcements: publish and manage system notices
- [x] Token management: online status, force logout
- [x] Multi-end login: toggle multi-client login modes
- [x] OAuth 2.0: built-in custom OAuth 2.0 provider
- [x] Plugin system: hot-pluggable, decoupled design
- [x] Scheduler: timed, async tasks and function calls
- [x] Code generator: generate, preview, write, and download
- [x] Operation logs: normal and error operations
- [x] Login logs: normal and error logins
- [x] Cache monitor: cache info and command stats
- [x] Service monitor: hardware info and status
- [x] API docs: interactive OpenAPI/Swagger UI

## Project Structure

::: file-tree

- backend
    - alembic/ database migrations
    - app
        - admin/ system backend
            - api/ interfaces
            - crud/ CRUD operations
            - model
                - __init__.py All model classes must be imported in this file
                - …
            - schema/ Data Transfer
            - service/ Services
            - tests/ Unit Tests
        - task/ Tasks
        - …
    - common/ Shared Resources
    - core/ Core Configuration
    - database/ Database Connections
    - log/ Logging
    - middleware/ Middleware
    - plugin Plugins
        - code_generator/ Code Generation
        - …
    - scripts/ Scripts
    - sql/ SQL Files
    - static/ Static Files
    - templates/ Template Files
    - utils/ Utility Tools
- deploy/ Server Deployment
- …

:::

## Contributors

<a href="https://github.com/fastapi-practices/fastapi_best_architecture/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fastapi-practices/fastapi_best_architecture"/>
</a>

## License

This project is licensed under the terms of the MIT License.

[![Stargazers over time](https://starchart.cc/fastapi-practices/fastapi_best_architecture.svg?variant=adaptive)](https://starchart.cc/fastapi-practices/fastapi_best_architecture)

## Special Thanks

- [downdawn](https://github.com/downdawn) for driving the creation of this project
- [lvright](https://github.com/lvright) for the thoughtfully designed logo
- [vuepress-theme-plume](https://github.com/pengzhanbo/vuepress-theme-plume) for powering the docs site
- FastAPI, SQLAlchemy, Pydantic, and other pioneers in open source
- All contributors, participants, and users of this project
- All sponsors across channels for their generous support
