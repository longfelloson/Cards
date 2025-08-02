from fastapi import APIRouter, Depends, status
from cashews import cache
from pydantic import UUID4

from auth.dependencies import CurrentUserDependency
from cache.keys import Key
from users.dependencies import UsersServiceDependency
from cache.constants import DAY_TTL, ONE_HOUR_TTL
from users.schemas import UserCreate, UsersFilter, UserUpdate, UserView

v1_router = APIRouter()


@v1_router.post(
    "",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
)
async def create_user(data: UserCreate, service: UsersServiceDependency):
    """Create a user with provided data"""
    user = await service.create(data=data)
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
@cache(ttl=ONE_HOUR_TTL, key=Key.USERS)
async def get_users(service: UsersServiceDependency, filter: UsersFilter = Depends()):
    """Get users by provided conditions"""
    users = await service.get_all(filter=filter)
    return users


@v1_router.get(
    "/{user_id}",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
)
@cache(ttl=DAY_TTL, key=Key.USER)
async def get_user(user_id: UUID4, service: UsersServiceDependency):
    """Get a user by its id"""
    user = await service.get(user_id=user_id)
    return user


@v1_router.patch(
    "/{user_id}",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
)
@cache.invalidate(Key.USER)
async def update_user(
    user_id: UUID4,
    data: UserUpdate,
    service: UsersServiceDependency,
):
    """Update a user with provided data"""
    user = await service.update(user_id=user_id, data=data)
    return user


@v1_router.delete(
    "/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@cache.invalidate(Key.USER)
async def delete_user(user_id: UUID4, service: UsersServiceDependency):
    """Delete a user by its id"""
    await service.delete(user_id=user_id)
