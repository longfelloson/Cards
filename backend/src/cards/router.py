from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from pydantic import UUID4

from auth.dependencies import CurrentUserDependency, get_current_user
from cache.constants import DAY_TTL, TWELVE_HOURS_TTL
from cards.schemas import CardCreate, CardsFilter, CardUpdate, CardView
from cards.service import service
from dependencies import UOWDependency

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CardView,
)
async def create_card(
    data: CardCreate,
    uow: UOWDependency,
    user: CurrentUserDependency,
):
    """Create a card with provided data"""
    card = await service.create(data=data, user_id=user.id, uow=uow)
    return card


@router.get(
    path="",
    response_model=list[CardView],
    status_code=status.HTTP_200_OK,
)
@cache(expire=TWELVE_HOURS_TTL)
async def get_cards(
    uow: UOWDependency,
    user: CurrentUserDependency,
    filter: CardsFilter = Depends(),
):
    """Get cards with provided conditions"""
    cards = await service.get_all(filter=filter, uow=uow, user_id=user.id)
    return cards


@router.get(
    path="/{card_id}",
    response_model=CardView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
@cache(expire=DAY_TTL)
async def get_card(card_id: UUID4, uow: UOWDependency):
    """Get a card by its ID"""
    card = await service.get(card_id=card_id, uow=uow)
    return card


@router.patch(
    "/{card_id}",
    response_model=CardView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def update_card(card_id: UUID4, data: CardUpdate, uow: UOWDependency):
    """Update a card with provided ID"""
    card = await service.update(card_id=card_id, data=data, uow=uow)
    return card


@router.delete(
    path="/{card_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def delete_card(card_id: UUID4, uow: UOWDependency):
    """Delete a card by its id"""
    await service.delete(card_id=card_id, uow=uow)
