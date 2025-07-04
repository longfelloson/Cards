from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from auth.dependencies import CurrentUserDependency, get_current_user
from dependencies import UOWDependency
from users.service import users_service
from users.schemas import UserCreate, UserUpdate, UserView, UsersFilter


router = APIRouter()


@router.post(
    "",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def create_user(data: UserCreate, uow: UOWDependency):
    """Create a user with provided data"""
    user = await users_service.create(data=data, uow=uow)
    return user


@router.get("/me", response_model=UserView, status_code=status.HTTP_200_OK)
async def get_current_user(user: CurrentUserDependency):
    """Get the current user"""
    return user


@router.get(
    "",
    response_model=list[UserView],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_users(uow: UOWDependency, filter: UsersFilter = Depends()):
    """Get users by provided conditions"""
    users = await users_service.get_all(filter=filter, uow=uow)
    return users


@router.get(
    "/{user_id}", response_model=UserView, dependencies=[Depends(get_current_user)]
)
async def get_user(user_id: UUID4, uow: UOWDependency):
    """Get a user by its id"""
    user = await users_service.get(user_id=user_id, uow=uow)
    return user


@router.patch(
    "/{user_id}",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def update_user(
    user_id: UUID4,
    data: UserUpdate,
    uow: UOWDependency,
):
    """Update a user with provided data"""
    user = await users_service.update(user_id=user_id, data=data, uow=uow)
    return user


@router.delete(
    "/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_user(user_id: UUID4, uow: UOWDependency):
    """Delete a user by its id"""
    await users_service.delete(user_id=user_id, uow=uow)
