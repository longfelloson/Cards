from redis.asyncio import Redis

from config import settings

redis_client = Redis().from_url(settings.redis.url)
