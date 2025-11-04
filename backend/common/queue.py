import asyncio

from asyncio import Queue


async def batch_dequeue(queue: Queue, max_items: int, timeout: float) -> list:
    """
    Retrieve multiple items from async queue

    :param queue: The `asyncio.Queue` queue to retrieve items from
    :param max_items: Maximum number of items to retrieve from the queue
    :param timeout: Total wait timeout in seconds
    :return:
    """
    items = []

    async def collector() -> None:
        while len(items) < max_items:
            item = await queue.get()
            items.append(item)

    try:
        await asyncio.wait_for(collector(), timeout=timeout)
    except asyncio.TimeoutError:
        pass

    return items
