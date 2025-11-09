import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from backend.common.log import log
from backend.core.conf import settings


class RedisCli(Redis):
    """Redis client"""

    def __init__(self) -> None:
        """Initialize Redis client"""
        super().__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            socket_connect_timeout=settings.REDIS_TIMEOUT,
            socket_keepalive=True,  # Keep connection alive
            health_check_interval=30,  # Health check interval
            decode_responses=True,  # Decode to utf-8
        )

    async def open(self) -> None:
        """Trigger initialization connection"""
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ Database redis connection timeout')
            sys.exit()
        except AuthenticationError:
            log.error('❌ Database redis authentication failed')
            sys.exit()
        except Exception as e:
            log.error('❌ Database redis connection error {}', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None, batch_size: int = 1000) -> None:
        """
        Delete all keys with specified prefix

        :param prefix: Key prefix to be deleted
        :param exclude: Key or list of keys to exclude
        :param batch_size: Batch size for deletion to prevent Redis overload from deleting too many keys at once
        :return:
        """
        exclude_set = set(exclude) if isinstance(exclude, list) else {exclude} if isinstance(exclude, str) else set()
        batch_keys = []

        async for key in self.scan_iter(match=f'{prefix}*'):
            if key not in exclude_set:
                batch_keys.append(key)

                if len(batch_keys) >= batch_size:
                    await self.delete(*batch_keys)
                    batch_keys.clear()

        if batch_keys:
            await self.delete(*batch_keys)

async def get_prefix(self, prefix: str, count: int = 100) -> list[str]:
        """
        Retrieve all keys with the specified prefix

        :param prefix: Key prefix to search for
        :param count: Number of items scanned per batch. Higher values increase scanning speed but consume more server resources.
        :return:
        """
        return [key async for key in self.scan_iter(match=f'{prefix}*', count=count)]


# Create redis client singleton
redis_client: RedisCli = RedisCli()
