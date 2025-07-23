from typing import Annotated

from fastapi import Depends

from cache.dependencies import StorageDependency
from dependencies import UOWDependency
from cards.service import CardsService


def get_cards_service(storage: StorageDependency, uow: UOWDependency) -> CardsService:
    service = CardsService(storage=storage, uow=uow)
    return service


CardsServiceDependency = Annotated[CardsService, Depends(get_cards_service)]
