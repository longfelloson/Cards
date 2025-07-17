from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from pydantic import UUID4

from auth.dependencies import CurrentUserDependency, PermissionsDependency
from decks.permissions import DeckOwnerPermission
from cache.namespaces import Namespace
from cache.constants import DAY_TTL, TWELVE_HOURS_TTL
from decks.schemas import DeckCreate, DecksFilter, DeckUpdate, DeckView
from decks.service import decks_service
from dependencies import UOWDependency

v1_router = APIRouter()


@v1_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=DeckView,
)
async def create_deck(
    data: DeckCreate,
    uow: UOWDependency,
    user: CurrentUserDependency,
):
    """Create a deck with provided data"""
    deck = await decks_service.create(
        data=data,
        user_id=user.id,
        uow=uow,
    )
    return deck


@v1_router.get(
    "/{deck_id}",
    response_model=DeckView,
    status_code=status.HTTP_200_OK,
)
@cache(expire=DAY_TTL, namespace=Namespace.DECK)
async def get_deck(deck_id: UUID4, uow: UOWDependency):
    """Get a deck by provided ID"""
    deck = await decks_service.get(deck_id=deck_id, uow=uow)
    return deck


@v1_router.get("", status_code=status.HTTP_200_OK, response_model=list[DeckView])
@cache(expire=TWELVE_HOURS_TTL, namespace=Namespace.DECKS)
async def get_decks(
    uow: UOWDependency,
    filter: DecksFilter = Depends(),
):
    """Get decks by given options"""
    decks = await decks_service.get_all(uow=uow, filter=filter)
    return decks


@v1_router.patch(
    "/{deck_id}",
    response_model=DeckView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(DeckOwnerPermission))],
)
async def update_deck(deck_id: UUID4, data: DeckUpdate, uow: UOWDependency):
    """Update a deck with provided ID"""
    deck = await decks_service.update(deck_id=deck_id, data=data, uow=uow)
    return deck


@v1_router.delete(
    "/{deck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(PermissionsDependency(DeckOwnerPermission))],
)
async def delete_deck(deck_id: UUID4, uow: UOWDependency):
    """Delete a deck by its ID"""
    await decks_service.delete(deck_id=deck_id, uow=uow)
