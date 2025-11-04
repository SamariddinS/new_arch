from time import sleep

from anyio import sleep as asleep

from backend.app.task.celery import celery_app


@celery_app.task(name='task_demo')
def task_demo() -> str:
    """Example task, simulating time-consuming operation"""
    sleep(30)
    return 'test async'


@celery_app.task(name='task_demo_async')
async def task_demo_async() -> str:
    """Async example task, simulating time-consuming operation"""
    await asleep(30)
    return 'test async'


@celery_app.task(name='task_demo_params')
async def task_demo_params(hello: str, world: str | None = None) -> str:
    """Parameter example task, simulating parameter passing operation"""
    await asleep(1)
    return hello + world
