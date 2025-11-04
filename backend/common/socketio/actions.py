from backend.common.socketio.server import sio


async def task_notification(msg: str) -> None:
    """
    Task notification

    :param msg: Notification message
    :return:
    """
    await sio.emit('task_notification', {'msg': msg})
