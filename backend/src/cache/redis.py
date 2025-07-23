from redis.asyncio import Redis

from config import settings


def get_redis_client() -> Redis:
    client = Redis().from_url(settings.redis.url)
    return client
