from typing import Annotated

from fastapi import Depends

from auth.dependencies import CurrentUserDependency
from cache.dependencies import StorageDependency
from deck_collections.service import CollectionsService
from dependencies import UOWDependency


async def get_collections_service(
    storage: StorageDependency,
    uow: UOWDependency,
    user: CurrentUserDependency,
) -> CollectionsService:
    service = CollectionsService(storage=storage, uow=uow, user=user)
    return service


CollectionsServiceDependency = Annotated[
    CollectionsService, Depends(get_collections_service)
]
