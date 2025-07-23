from typing import Annotated

from fastapi import Depends
from dependencies import UOWDependency
from cache.dependencies import StorageDependency
from decks.service import DeckService


def get_decks_service(storage: StorageDependency, uow: UOWDependency) -> DeckService:
    service = DeckService(storage=storage, uow=uow)
    return service


DecksServiceDependency = Annotated[DeckService, Depends(get_decks_service)]
