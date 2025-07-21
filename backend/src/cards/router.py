from fastapi import APIRouter, Depends, Request, status
from fastapi_cache.decorator import cache
from pydantic import UUID4

from auth.dependencies import PermissionsDependency
from cards.permissions import (
    CardOwnerPermission,
    CardViewPermission,
    CardsViewPermission,
)
from cache.namespaces import Namespace
from cache.constants import DAY_TTL, TWELVE_HOURS_TTL
from cards.schemas import CardCreate, CardsFilter, CardUpdate, CardView
from cards.service import cards_service
from dependencies import UOWDependency

v1_router = APIRouter()


@v1_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CardView,
)
async def create_card(
    request: Request,
    data: CardCreate,
    uow: UOWDependency,
):
    """Create a card with provided data"""
    card = await cards_service.create(data=data, user_id=request.user.id, uow=uow)
    return card


@v1_router.get(
    path="",
    response_model=list[CardView],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(CardsViewPermission))],
)
@cache(expire=TWELVE_HOURS_TTL, namespace=Namespace.CARDS)
async def get_cards(uow: UOWDependency, filter: CardsFilter = Depends()):
    """Get cards with provided conditions"""
    cards = await cards_service.get_all(filter=filter, uow=uow)
    return cards


@v1_router.get(
    path="/{card_id}",
    response_model=CardView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(CardViewPermission))],
)
@cache(expire=DAY_TTL, namespace=Namespace.CARD)
async def get_card(card_id: UUID4, uow: UOWDependency):
    """Get a card by its ID"""
    card = await cards_service.get(card_id=card_id, uow=uow)
    return card


@v1_router.patch(
    "/{card_id}",
    response_model=CardView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(CardOwnerPermission))],
)
async def update_card(card_id: UUID4, data: CardUpdate, uow: UOWDependency):
    """Update a card with provided ID"""
    card = await cards_service.update(card_id=card_id, data=data, uow=uow)
    return card


@v1_router.delete(
    path="/{card_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(PermissionsDependency(CardOwnerPermission))],
)
async def delete_card(card_id: UUID4, uow: UOWDependency):
    """Delete a card by its id"""
    await cards_service.delete(card_id=card_id, uow=uow)
