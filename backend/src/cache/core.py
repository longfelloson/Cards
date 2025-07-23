import asyncio

from cache.keys import Key


class Storage:
    def __init__(self, *, client):
        self.keys = Key
        self.client = client

    async def clear_cache_by_key(self, *, key: Key):
        keys = []
        async for key in self.client.scan_iter(key + "*"):
            keys.append(key)

        if keys:
            await asyncio.gather(*(self.client.delete(key) for key in keys))

    async def clear_cache_by_keys(self, *keys: Key) -> None:
        for key in keys:
            await self.clear_cache_by_key(key=key)
            