from fastapi import APIRouter, Depends, status
from cashews import cache
from pydantic import UUID4

from cache.keys import Key
from cache.constants import DAY_TTL, ONE_HOUR_TTL
from cards.schemas import CardCreate, CardsFilter, CardUpdate, CardView
from cards.dependencies import CardsServiceDependency

v1_router = APIRouter()


@v1_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CardView,
)
async def create_card(data: CardCreate, service: CardsServiceDependency):
    """Create a card with provided data"""
    card = await service.create(data=data)
    return card


@v1_router.get(
    path="",
    response_model=list[CardView],
    status_code=status.HTTP_200_OK,
)
@cache(ttl=ONE_HOUR_TTL, key=Key.CARDS)
async def get_cards(
    service: CardsServiceDependency,
    filter: CardsFilter = Depends(),
):
    """Get cards with provided conditions"""
    cards = await service.get_all(filter=filter)
    return cards


@v1_router.get(
    path="/{card_id}",
    response_model=CardView,
    status_code=status.HTTP_200_OK,
)
@cache(ttl=DAY_TTL, key=Key.CARD)
async def get_card(card_id: UUID4, service: CardsServiceDependency):
    """Get a card by its ID"""
    card = await service.get(card_id=card_id)
    return card


@v1_router.patch(
    "/{card_id}",
    response_model=CardView,
    status_code=status.HTTP_200_OK,
)
@cache.invalidate(Key.CARD)
async def update_card(
    card_id: UUID4, data: CardUpdate, service: CardsServiceDependency
):
    """Update a card with provided ID"""
    card = await service.update(card_id=card_id, data=data)
    return card


@v1_router.delete(
    path="/{card_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@cache.invalidate(Key.CARD)
async def delete_card(card_id: UUID4, service: CardsServiceDependency):
    """Delete a card by its id"""
    await service.delete(card_id=card_id)
