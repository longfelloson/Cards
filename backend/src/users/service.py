from typing import Optional

from pydantic import UUID4

from auth.password import get_hashed_password
from service import AbstractService
from users.exceptions import UserAlreadyExists, UserNotFound
from unit_of_work import UnitOfWork
from users.models import User
from users.schemas import UserCreate, UserFilter, UserUpdate, UsersFilter


class UsersService(AbstractService):
    async def create(self, *, data: UserCreate, uow: UnitOfWork) -> User:
        """Creates a user with provided data"""
        data.password = get_hashed_password(data.password)
        async with uow:
            user_filter = UserFilter(email=data.email)
            user = await self.get_by(filter=user_filter, uow=uow)
            if user:
                raise UserAlreadyExists()
            user = await uow.users.create(data=data)
            return user

    async def get(
        self,
        *,
        user_id: UUID4,
        uow: UnitOfWork,
    ) -> User:
        """Get a user by its ID"""
        async with uow:
            user = await uow.users.get(id=user_id)
            if not user:
                raise UserNotFound()
            return user

    async def get_by(self, *, filter: UserFilter, uow: UnitOfWork) -> Optional[User]:
        """Get a user by provided filter"""
        async with uow:
            user = await uow.users.get_by(filter=filter)
            return user

    async def get_all(
        self, *, filter: UsersFilter, uow: UnitOfWork
    ) -> list[Optional[User]]:
        """Get users by provided conditions"""
        async with uow:
            users = await uow.users.get_all(filter=filter)
            return users

    async def update(self, user_id: UUID4, data: UserUpdate, uow: UnitOfWork) -> User:
        """Update a user with provided data by its id"""
        async with uow:
            user = await self.get(user_id=user_id, uow=uow)
            update_data = data.model_dump(exclude_none=True)
            updated_user = await uow.users.update(obj=user, data=update_data)
            return updated_user

    async def delete(self, *, user_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a user by its id"""
        async with uow:
            user = await self.get(user_id=user_id)
            await uow.users.delete(obj=user)


users_service = UsersService()
