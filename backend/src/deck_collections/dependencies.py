from typing import Annotated

from fastapi import Depends

from cache.dependencies import StorageDependency
from deck_collections.service import CollectionsService


def get_collections_service(storage: StorageDependency) -> CollectionsService:
    service = CollectionsService(storage=storage)
    return service


CollectionsServiceDependency = Annotated[
    CollectionsService, Depends(get_collections_service)
]
