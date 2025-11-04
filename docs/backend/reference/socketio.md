---
title: socketio
---

## Why not use WS?

WebSocket is already integrated into fastapi and can be used directly, so why use Socket.IO? There are many reasons, but it can be simply summarized as Socket.IO offering greater functionality and stability. If you use ws, you might have to manually wrap many things, but Socket.IO has essentially written all that for you. So, why not?

## What is Socket.IO?

Socket.IO is a transport protocol that enables real-time, bidirectional, event-driven communication between clients and servers.

Without Socket.IO:

Your leader is out of town and has assigned you an urgent task. This task is equivalent to an event, but you can't complete it quickly. However, your leader will soon ask you how it's going (polling). You're annoyed and don't want to respond (delayed reaction).

When using Socket.IO:

Your leader is sitting right beside you, your productivity skyrockets, you finish the task immediately, and report completion verbally on the spot—he hears it instantly (in real time).

## Integrated

In FBA, you can examine the local Socket.IO implementation in the `backend/common/socketio/` directory, which contains two files.

`actions.py`: This file is primarily used to define global events, enabling centralized event management.

`server.py`: This file contains the standard server implementation in FBA, including Socket.IO authorized connections.

However, these are not the primary integration code. We can navigate to the `backend/core/register.py` file and locate the following method:

```python
def register_socket_app(app: FastAPI):
    """
    socket application

    :param app:
    :return:
    """
    from backend.common.socketio.server import sio

    socket_app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=app,
        # Do not delete this configuration.：https://github.com/pyropy/fastapi-socketio/issues/51
        socketio_path='/ws/socket.io',
    )
    app.mount('/ws', socket_app)
```

We define the `python-socketio` ASGI application by passing both the socketio and fastapi applications as parameters. At this point, you have created a socket application.
Then, using FastAPI's built-in mounting functionality, we mount the socket application into the FastAPI application. With that, you have completed integrating FastAPI with Socket.IO.
