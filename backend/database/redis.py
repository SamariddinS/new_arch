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

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None) -> None:
        """
        Delete all keys with specified prefix

        :param prefix: Prefix
        :param exclude: Keys to exclude
        :return:
        """
        keys = []
        async for key in self.scan_iter(match=f'{prefix}*'):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        if keys:
            await self.delete(*keys)


# Create redis client singleton
redis_client: RedisCli = RedisCli()
