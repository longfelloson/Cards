from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from pydantic import UUID4

from auth.dependencies import CurrentUserDependency, get_current_user
from cache.constants import DAY_TTL, TWELVE_HOURS_TTL
from decks.schemas import DeckCreate, DecksFilter, DeckUpdate, DeckView
from decks.service import service
from dependencies import UOWDependency

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=DeckView,
)
async def create_deck(
    data: DeckCreate, uow: UOWDependency, user: CurrentUserDependency
):
    """Create a deck with provided data"""
    deck = await service.create(
        data=data,
        user_id=user.id,
        uow=uow,
    )
    return deck


@router.get(
    "/{deck_id}",
    response_model=DeckView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
@cache(expire=DAY_TTL)
async def get_deck(deck_id: UUID4, uow: UOWDependency):
    """Get a deck by provided ID"""
    deck = await service.get(deck_id=deck_id, uow=uow)
    return deck


@router.get("", status_code=status.HTTP_200_OK, response_model=list[DeckView])
@cache(expire=TWELVE_HOURS_TTL)
async def get_decks(
    uow: UOWDependency,
    user: CurrentUserDependency,
    filter: DecksFilter = Depends(),
):
    """Get decks by given options"""
    decks = await service.get_all(uow=uow, filter=filter, user_id=user.id)
    return decks


@router.patch(
    "/{deck_id}",
    response_model=DeckView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def update_deck(deck_id: UUID4, data: DeckUpdate, uow: UOWDependency):
    """Update a deck with provided ID"""
    deck = await service.update(deck_id=deck_id, data=data, uow=uow)
    return deck


@router.delete(
    "/{deck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_deck(deck_id: UUID4, uow: UOWDependency):
    """Delete a deck by its ID"""
    await service.delete(deck_id=deck_id, uow=uow)
