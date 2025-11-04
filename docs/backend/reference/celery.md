---
title: Celery
---

For many, Celery has a steep learning curve and the documentation (while comprehensive) can feel dense. Let’s break the barriers and embrace Celery.

## Why Celery?

Celery is a distributed task queue for Python. It excels at heavy or complex tasks because it runs in separate processes, not sharing the main app’s process. Tasks are handled asynchronously without consuming main app resources, improving responsiveness and throughput. See our migration discussion: #225.

## Broker

From the Celery glossary, a broker is described as:

> [Enterprise Integration Model ](https://www.enterpriseintegrationpatterns.com/)
> [Message Broker](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageBroker.html)
> Defined as an architectural component that can receive messages from multiple destinations.
> [News](https://docs.celeryq.dev/projects/celery-enhancement-proposals/en/latest/glossary.html?highlight=broker#term-Message)
> ，Determine the correct destination and route the message to the appropriate channel.

In Celery, the broker stores scheduled task messages and routes them; it does not execute tasks. Workers pull from the broker to run tasks, making the broker essential.

Supported brokers are listed in the docs. fba selects Redis in dev and RabbitMQ in prod based on `ENVIRONMENT`.

```python
@model_validator(mode='before')
@classmethod
def validate_celery_broker(cls, values):
    if values['ENVIRONMENT'] == 'prod':
        # use redis in dev; rabbitmq in prod
        values['CELERY_BROKER'] = 'rabbitmq'
    return values
```

## Worker

Workers execute scheduled tasks. They listen to the broker and pull tasks to run.

Multiple workers can run for distributed processing. By default, Celery starts as many worker processes as CPU cores (e.g., 16 cores -> 16 workers).

If no workers are running, messages accumulate in the broker until a worker consumes them.

## Backend

The [Tasks Page](https://docs.celeryq.dev/en/v5.4.0/userguide/tasks.html#result-backends) in the Celery User Guide for Backend
The following is an introduction:

> If you want to track tasks or need return values, Celery must store or send the status somewhere for later retrieval. Several built-in result backends are available for you to choose from: SQLAlchemy/Django
> ORM, Memcached, RabbitMQ/QPid (RPC), and Redis—you can also define your own backend; no single backend fits every use case perfectly.
> You should understand the strengths and weaknesses of each backend, then choose the one that best suits your needs.

fba uses a database as the default result backend.

Scenario: track and return async task results.

Suppose you build a long-running report generation task. The frontend triggers an API, FastAPI enqueues a Celery task, and returns immediately. The task runs outside the main app. Once done, FastAPI can return results which the frontend then consumes.

Here, results are stored in the backend after completion (pending states aren’t persisted by all backends). Using a backend is optional unless you need to retrieve results.

## Elegant integration

fba integrates Celery with minimal boilerplate. Configure it and go. We also support defining tasks as async functions. Note: official async task support was added only in Celery 6.0.

See `backend/app/task` for the Celery app. You can delete it if using another task app.

Inside `task`, `celery.py` initializes Celery and its startup parameters. No edits required. Video walkthrough: Celery Integration.

## Advanced usage

### Execution pools

Choose a pool based on workload characteristics:

::: tabs

@tab prefork

CPU-bound tasks (image processing, computations)

```bash
celery -A app.task.celery worker -l info -P prefork
```

@tab threads

No async needed

```bash
celery -A app.task.celery worker -l info -P threads
```

@tab gevent

I/O-bound tasks needing async

```bash
celery -A app.task.celery worker -l info -P gevent
```

:::

### Concurrency

Set worker concurrency with `-c`:

```bash
celery -A app.task.celery worker -l info -P gevent -c 1000
```

::: tabs

@tab prefork

Prefork: ~1–2 x CPU cores

@tab threads

Threads: ~2–10 x CPU cores

@tab gevent

Gevent: ~100–1000

:::

### Queues

Define queues in Celery config:

```python
app.conf.task_queues = (
    Queue('cpu_bind', routing_key='cpu'),  # CPU-bound
    Queue('io_bind', routing_key='io'),    # IO-bound
    Queue('all_in'),                       # simple queue without routing key
)
```

Start workers for specific queues with `-Q`:

```bash
celery -A app.task.celery worker -l info -P gevent -c 1000 -Q cpu_bind  # CPU worker
celery -A app.task.celery worker -l info -P gevent -c 1000 -Q io_bind   # IO worker
```

Assign a queue when defining a task:

```python
@celery_app(queue='io_bind')
async def io_bind_task():
    ...
```
