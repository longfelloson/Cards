from typing import Annotated

from fastapi import Depends

from cache.core import Storage
from cache.redis import get_redis_client


def get_storage(client = Depends(get_redis_client)) -> Storage:
    storage = Storage(client=client)
    return storage


StorageDependency = Annotated[Storage, Depends(get_storage)]
