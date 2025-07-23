from fastapi import APIRouter, Depends, Request, status
from fastapi_cache.decorator import cache
from pydantic import UUID4

from auth.dependencies import PermissionsDependency
from decks.dependencies import DecksServiceDependency
from decks.permissions import (
    DeckOwnerPermission,
    DeckViewPermission,
    DecksViewPermission,
)
from cache.namespaces import Namespace
from cache.constants import DAY_TTL, TWELVE_HOURS_TTL
from decks.schemas import DeckCreate, DecksFilter, DeckUpdate, DeckView

v1_router = APIRouter()


@v1_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=DeckView,
)
async def create_deck(
    request: Request, data: DeckCreate, service: DecksServiceDependency
):
    """Create a deck with provided data"""
    deck = await service.create(data=data, user_id=request.user.id)
    return deck


@v1_router.get(
    "/{deck_id}",
    response_model=DeckView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(DeckViewPermission))],
)
@cache(expire=DAY_TTL, namespace=Namespace.DECK)
async def get_deck(deck_id: UUID4, service: DecksServiceDependency):
    """Get a deck by provided ID"""
    deck = await service.get(deck_id=deck_id)
    return deck


@v1_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[DeckView],
    dependencies=[Depends(PermissionsDependency(DecksViewPermission))],
)
@cache(expire=TWELVE_HOURS_TTL, namespace=Namespace.DECKS)
async def get_decks(service: DecksServiceDependency, filter: DecksFilter = Depends()):
    """Get decks by given options"""
    decks = await service.get_all(filter=filter)
    return decks


@v1_router.patch(
    "/{deck_id}",
    response_model=DeckView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(DeckOwnerPermission))],
)
async def update_deck(
    deck_id: UUID4, data: DeckUpdate, service: DecksServiceDependency,
):
    """Update a deck with provided ID"""
    deck = await service.update(deck_id=deck_id, data=data)
    return deck


@v1_router.delete(
    "/{deck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(PermissionsDependency(DeckOwnerPermission))],
)
async def delete_deck(deck_id: UUID4, service: DecksServiceDependency):
    """Delete a deck by its ID"""
    await service.delete(deck_id=deck_id)
