from typing import Optional

from auth.password import get_hashed_password
from auth.verification.service import verification_service
from pydantic import UUID4
from service import AbstractService
from unit_of_work import UnitOfWork
from users.exceptions import UserAlreadyExistsException, UserNotFoundException
from users.models import User
from users.schemas import UserCreate, UserFilter, UsersFilter, UserUpdate


class UsersService(AbstractService):
    async def create(self, *, data: UserCreate, uow: UnitOfWork) -> User:
        """Creates a user with provided data"""
        data.password = get_hashed_password(data.password)
        async with uow:
            user_filter = UserFilter(email=data.email)
            user = await self.get_by(filter=user_filter, uow=uow)
            if user:
                raise UserAlreadyExistsException()
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
                raise UserNotFoundException()
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

    async def update(
        self, *, user_id: UUID4, data: UserUpdate, uow: UnitOfWork
    ) -> Optional[User]:
        """Updates user if data.verify_email wasn't provided. if it was provided -
        send verification email. If email was provided and verify_email wasn't -
        confirms the email and updates the user

        Returns:
            User: updated user if fields to update were provided otherwise the
            same user
        """
        async with uow:
            user = await self.get(user_id=user_id, uow=uow)
            if data.verify:
                await verification_service.verify(
                    user=user,
                    uow=uow,
                    new_email=data.email,
                    new_password=data.password,
                )
                return user
            elif data.verification_token:
                await verification_service.confirm(
                    token=data.verification_token, uow=uow
                )

            if data.password:
                data.password = get_hashed_password(data.password)

            if not data.are_new_column_values_provided(user):
                return user

            update_data = data.model_dump(exclude_none=True)
            updated_user = await uow.users.update(obj=user, data=update_data)

            return updated_user

    async def delete(self, *, user_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a user by its id"""
        async with uow:
            await uow.users.delete(obj_id=user_id)


users_service = UsersService()
