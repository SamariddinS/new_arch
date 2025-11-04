## Task Introduction

The current task system is implemented using Celery. For implementation details, please refer to [#225](https://github.com/fastapi-practices/fastapi_best_architecture/discussions/225)

## Scheduled Tasks

Write scheduled task code in the `backend/app/task/tasks/beat.py` file

### Simple Tasks

Write task code in the `backend/app/task/tasks/tasks.py` file

### Hierarchical Tasks

If you want to organize tasks into directory hierarchies to make the task structure clearer, you can create any directory, but please note:

1. Create a Python package directory under `backend/app/task/tasks`
2. After creating the directory, make sure to update `CELERY_TASKS_PACKAGES` in the `conf.py` configuration and add the new directory module path to this list
3. In the new directory, make sure to add a `tasks.py` file and write the task code in this file

## Message Broker

You can control the message broker selection through `CELERY_BROKER`. It supports redis and rabbitmq

For local debugging, it's recommended to use redis

For production environment, rabbitmq must be used
