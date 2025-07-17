from auth.dependencies import PermissionsDependency
from auth.rbac.dependencies import RoleAccessDependency
from deck_collections.permissions import CollectionOwnerPermission
from cache.namespaces import Namespace
from cache.constants import DAY_TTL, TWELVE_HOURS_TTL
from deck_collections.schemas import (
    CollectionCreate,
    CollectionsFilter,
    CollectionUpdate,
    CollectionView,
)
from deck_collections.service import collections_service
from dependencies import UOWDependency
from fastapi import APIRouter, Depends, Request, status
from fastapi_cache.decorator import cache
from pydantic import UUID4

v1_router = APIRouter(dependencies=[Depends(RoleAccessDependency)])


@v1_router.post("", response_model=CollectionView, status_code=status.HTTP_201_CREATED)
async def create_collection(
    request: Request,
    data: CollectionCreate,
    uow: UOWDependency,
):
    """Create a collection with provided data"""
    collection = await collections_service.create(
        data=data, user_id=request.user.id, uow=uow
    )
    return collection


@v1_router.get(
    "/{collection_id}",
    response_model=CollectionView,
    status_code=status.HTTP_200_OK,
)
@cache(expire=DAY_TTL, namespace=Namespace.COLLECTION)
async def get_collection(collection_id: UUID4, uow: UOWDependency):
    """Get a collection by its id"""
    collection = await collections_service.get(collection_id=collection_id, uow=uow)
    return collection


@v1_router.get(
    "",
    response_model=list[CollectionView],
    status_code=status.HTTP_200_OK,
)
@cache(expire=TWELVE_HOURS_TTL, namespace=Namespace.COLLECTIONS)
async def get_collections(
    request: Request,
    uow: UOWDependency,
    filter: CollectionsFilter = Depends(),
):
    """Get collections by provided conditions"""
    collections = await collections_service.get_all(
        filter=filter,
        uow=uow,
        user_id=request.user.id,
    )
    return collections


@v1_router.patch(
    "/{collection_id}",
    response_model=CollectionView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(CollectionOwnerPermission))],
)
async def update_collection(
    collection_id: UUID4, data: CollectionUpdate, uow: UOWDependency
):
    """Update a collection by provided data"""
    collection = await collections_service.update(
        collection_id=collection_id, data=data, uow=uow
    )
    return collection


@v1_router.delete(
    "/{collection_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(PermissionsDependency(CollectionOwnerPermission))],
)
async def delete_collection(collection_id: UUID4, uow: UOWDependency):
    """Delete a collection by its id"""
    await collections_service.delete(collection_id=collection_id, uow=uow)
