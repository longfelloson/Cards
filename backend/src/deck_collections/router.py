from fastapi import APIRouter, Depends, status
from cashews import cache
from pydantic import UUID4

from cache.keys import Key
from deck_collections.dependencies import CollectionsServiceDependency
from cache.constants import DAY_TTL, ONE_HOUR_TTL
from deck_collections.schemas import (
    CollectionCreate,
    CollectionsFilter,
    CollectionUpdate,
    CollectionView,
)

v1_router = APIRouter()


@v1_router.post("", response_model=CollectionView, status_code=status.HTTP_201_CREATED)
async def create_collection(
    data: CollectionCreate, service: CollectionsServiceDependency
):
    """Create a collection with provided data"""
    collection = await service.create(data=data)
    return collection


@v1_router.get(
    "/{collection_id}",
    response_model=CollectionView,
    status_code=status.HTTP_200_OK,
)
@cache(ttl=DAY_TTL, key=Key.COLLECTION)
async def get_collection(collection_id: UUID4, service: CollectionsServiceDependency):
    """Get a collection by its id"""
    collection = await service.get(collection_id=collection_id)
    return collection


@v1_router.get(
    "",
    response_model=list[CollectionView],
    status_code=status.HTTP_200_OK,
)
@cache(ttl=ONE_HOUR_TTL, key=Key.COLLECTIONS)
async def get_collections(
    service: CollectionsServiceDependency,
    filter: CollectionsFilter = Depends(),
):
    """Get collections by provided conditions"""
    collections = await service.get_all(filter=filter)
    return collections


@v1_router.patch(
    "/{collection_id}",
    response_model=CollectionView,
    status_code=status.HTTP_200_OK,
)
@cache.invalidate(Key.COLLECTION)
async def update_collection(
    collection_id: UUID4,
    data: CollectionUpdate,
    service: CollectionsServiceDependency,
):
    """Update a collection by provided data"""
    collection = await service.update(collection_id=collection_id, data=data)
    return collection


@v1_router.delete(
    "/{collection_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@cache.invalidate(Key.COLLECTION)
async def delete_collection(
    collection_id: UUID4, service: CollectionsServiceDependency
):
    """Delete a collection by its id"""
    await service.delete(collection_id=collection_id)
