from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from auth.dependencies import CurrentUserDependency, get_current_user
from deck_collections.service import service
from dependencies import UOWDependency
from deck_collections.schemas import (
    CollectionCreate,
    CollectionUpdate,
    CollectionView,
    CollectionsFilter,
)


router = APIRouter()


@router.post("", response_model=CollectionView, status_code=status.HTTP_201_CREATED)
async def create_collection(
    data: CollectionCreate,
    uow: UOWDependency,
    user: CurrentUserDependency,
):
    """Create a collection with provided data"""
    collection = await service.create(data=data, uow=uow)
    return collection


@router.get(
    "/{collection_id}",
    response_model=CollectionView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_collection(collection_id: UUID4, uow: UOWDependency):
    """Get a collection by its id"""
    collection = await service.get(collection_id=collection_id, uow=uow)
    return collection


@router.get(
    "",
    response_model=list[CollectionView],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_collections(
    uow: UOWDependency,
    user: CurrentUserDependency,
    filter: CollectionsFilter = Depends(),
):
    """Get collections by provided conditions"""
    collections = await service.get_all(filter=filter, uow=uow, user_id=user.id)
    return collections


@router.patch(
    "/{collection_id}",
    response_model=CollectionView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def update_collection(
    collection_id: UUID4, data: CollectionUpdate, uow: UOWDependency
):
    """Update a collection by provided data"""
    collection = await service.update(collection_id=collection_id, data=data, uow=uow)
    return collection


@router.delete(
    "/{collection_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def delete_collection(collection_id: UUID4, uow: UOWDependency):
    """Delete a collection by its id"""
    await service.delete(collection_id=collection_id, uow=uow)
