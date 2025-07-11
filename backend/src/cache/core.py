import asyncio
from typing import Sequence
from cache.keys import Key

from cache.redis import redis_client


class Storage:
    def __init__(self, *, client, keys):
        self.keys = keys
        self.client = client

    async def clear_cache(self, *, key: Key):
        keys = []
        async for key in self.client.scan_iter(key + "*"):
            keys.append(key)

        if keys:
            await asyncio.gather(*(self.client.delete(key) for key in keys))

    async def delete_related_cache(self, *keys: Sequence[Key]) -> None:
        for key in keys:
            await self.clear_cache(key=key)


storage = Storage(client=redis_client, keys=Key)
