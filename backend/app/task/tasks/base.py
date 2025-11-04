import asyncio

from typing import Any

from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from backend.common.socketio.actions import task_notification
from backend.core.conf import settings


class TaskBase(Task):
    """Celery task base class"""

    autoretry_for = (SQLAlchemyError,)
    max_retries = settings.CELERY_TASK_MAX_RETRIES

    async def before_start(self, task_id: str, args, kwargs) -> None:  # noqa: ANN001
        """
        Hook executed before task starts

        :param task_id: Task ID
        :return:
        """
        await task_notification(msg=f'Task {task_id} started execution')

    async def on_success(self, retval: Any, task_id: str, args, kwargs) -> None:  # noqa: ANN001
        """
        Hook executed after task succeeds

        :param retval: Task return value
        :param task_id: Task ID
        :return:
        """
        await task_notification(msg=f'Task {task_id} executed successfully')

    def on_failure(self, exc: Exception, task_id: str, args, kwargs, einfo) -> None:  # noqa: ANN001
        """
        Hook executed after task fails

        :param exc: Exception object
        :param task_id: Task ID
        :param einfo: Exception information
        :return:
        """
        asyncio.create_task(task_notification(msg=f'Task {task_id} execution failed'))
