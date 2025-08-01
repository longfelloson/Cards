from typing import List, Optional

from pydantic import UUID4
from sqlalchemy.exc import SQLAlchemyError

from auth.password import get_hashed_password
from service import AbstractService
from users.exceptions import UserAlreadyExistsException, UserNotFoundException
from users.models import User
from users.schemas import UserCreate, UserFilter, UsersFilter, UserUpdate
from logger import logger


class UsersService(AbstractService):
    def __init__(self, *, verification_service, storage, uow, user: User):
        self.verification_service = verification_service
        self.storage = storage
        self.uow = uow
        self.user = user

    async def create(self, *, data: UserCreate) -> User:
        """Creates a user with provided data"""
        data.password = get_hashed_password(data.password)
        try:
            async with self.uow:
                user_filter = UserFilter(email=data.email)
                user = await self.get_by(filter=user_filter)
                if user:
                    raise UserAlreadyExistsException()
                user = await self.uow.users.create(data=data)

                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(f"Failed to create a user with data = {data}:", exc_info=True)
            raise exc
        else:
            return user

    async def get(self, *, user_id: UUID4) -> User:
        """Get a user by its ID"""
        try:
            async with self.uow:
                user = await self.uow.users.get(id=user_id)
                if not user:
                    raise UserNotFoundException()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to get a user with user_id = {user_id}:", exc_info=True
            )
            raise exc
        else:
            return user

    async def get_by(self, *, filter: UserFilter) -> Optional[User]:
        """Get a user by provided filter"""
        try:
            async with self.uow:
                user = await self.uow.users.get_by(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(f"Failed to get a user with filter = {filter}:", exc_info=True)
            raise exc
        else:
            return user

    async def get_all(self, *, filter: UsersFilter) -> List[Optional[User]]:
        """Get users by provided conditions"""
        try:
            async with self.uow:
                users = await self.uow.users.get_all(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(f"Failed to get users with filter = {filter}:", exc_info=True)
            raise exc
        else:
            return users

    async def update(self, *, user_id: UUID4, data: UserUpdate) -> Optional[User]:
        """Updates user if data.verify_email wasn't provided. if it was provided -
        send verification email. If email was provided and verify_email wasn't -
        confirms the email and updates the user

        Returns:
            User: updated user if fields to update were provided otherwise the
            same user
        """
        try:
            async with self.uow:
                user = await self.get(user_id=user_id)
                if data.verify:
                    await self.verification_service.verify(
                        user=user,
                        new_email=data.email,
                        new_password=data.password,
                    )
                    return user
                elif data.verification_token:
                    await self.verification_service.confirm(
                        token=data.verification_token
                    )

                if data.password:
                    data.password = get_hashed_password(data.password)

                if not data.are_new_column_values_provided(user):
                    return user

                update_data = data.model_dump(exclude_none=True)
                updated_user = await self.uow.users.update(obj=user, data=update_data)

                await self.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to update a user with data = {data} and user_id = {user_id}:",
                exc_info=True,
            )
            raise exc
        else:
            return updated_user

    async def delete(self, *, user_id: UUID4) -> None:
        """Delete a user by its id"""
        try:
            async with self.uow:
                await self.uow.users.delete(obj_id=user_id)
                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to delete a user with user_id = {user_id}:", exc_info=True
            )
            raise exc
