from typing import Annotated

from fastapi import Depends
from auth.dependencies import CurrentUserDependency
from dependencies import UOWDependency
from cache.dependencies import StorageDependency
from decks.service import DeckService


async def get_decks_service(
    storage: StorageDependency, uow: UOWDependency, user: CurrentUserDependency
) -> DeckService:
    service = DeckService(storage=storage, uow=uow, user=user)
    return service


DecksServiceDependency = Annotated[DeckService, Depends(get_decks_service)]
