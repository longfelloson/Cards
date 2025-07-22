from auth.dependencies import CurrentUserDependency, PermissionsDependency
from users.permissions import UserOwnerPermission
from cache.namespaces import Namespace
from cache.constants import DAY_TTL, TWELVE_HOURS_TTL
from dependencies import UOWDependency
from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from pydantic import UUID4
from users.schemas import UserCreate, UsersFilter, UserUpdate, UserView
from users.service import users_service

v1_router = APIRouter()


@v1_router.post(
    "",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
)
async def create_user(data: UserCreate, uow: UOWDependency):
    """Create a user with provided data"""
    user = await users_service.create(data=data, uow=uow)
    return user


@v1_router.get(
    "/me",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
)
async def get_me(user: CurrentUserDependency):
    """Get the current user"""
    return user


@v1_router.get(
    "",
    response_model=list[UserView],
    status_code=status.HTTP_200_OK,
)
@cache(expire=TWELVE_HOURS_TTL, namespace=Namespace.USERS)
async def get_users(uow: UOWDependency, filter: UsersFilter = Depends()):
    """Get users by provided conditions"""
    users = await users_service.get_all(filter=filter, uow=uow)
    return users


@v1_router.get(
    "/{user_id}",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(UserOwnerPermission))],
)
@cache(expire=DAY_TTL, namespace=Namespace.USER)
async def get_user(user_id: UUID4, uow: UOWDependency):
    """Get a user by its id"""
    user = await users_service.get(user_id=user_id, uow=uow)
    return user


@v1_router.patch(
    "/{user_id}",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(PermissionsDependency(UserOwnerPermission))],
)
async def update_user(
    user_id: UUID4,
    data: UserUpdate,
    uow: UOWDependency,
):
    """Update a user with provided data"""
    user = await users_service.update(user_id=user_id, data=data, uow=uow)
    return user


@v1_router.delete(
    "/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(PermissionsDependency(UserOwnerPermission))],
)
async def delete_user(user_id: UUID4, uow: UOWDependency):
    """Delete a user by its id"""
    await users_service.delete(user_id=user_id, uow=uow)
