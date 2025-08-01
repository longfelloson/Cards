from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from pydantic import UUID4

from auth.permissions.core import OwnerPermission
from cache.core import Storage
from decks.permissions import DeckViewPermission, DecksViewPermission
from logger import logger
from decks.exceptions import DeckAlreadyExistsException, DeckNotFoundException
from decks.models import Deck
from decks.schemas import DeckCreate, DeckFilter, DecksFilter, DeckUpdate
from service import AbstractService
from unit_of_work import UnitOfWork
from users.models import User


class DeckService(AbstractService):
    def __init__(self, *, storage, uow, user):
        self.storage: Storage = storage
        self.uow: UnitOfWork = uow
        self.user: User = user

    async def create(self, *, data: DeckCreate) -> Deck:
        """Create a deck with provided data"""
        try:
            async with self.uow:
                deck_filter = DeckFilter(name=data.name)
                deck = await self.get_by(filter=deck_filter)
                if deck:
                    raise DeckAlreadyExistsException()

                deck: Deck = await self.uow.decks.create(data=data)

                await self.uow.commit()
        except SQLAlchemyError:
            logger.error(
                f"Failed to create a deck with user_id = {self.user.id} and data = {data}",
                exc_info=True,
            )
            raise
        else:
            return deck

    async def get(self, *, deck_id: UUID4) -> Deck:
        """Get a deck with provided ID and check permissions

        Raises:
            DeckNotFoundException: if a deck was not found
            NotEnoughPermissionsException: if a user didn't have enough permissions to view
        """
        try:
            async with self.uow:
                deck = await self.uow.decks.get(id=deck_id)
        except SQLAlchemyError:
            logger.error(
                f"Failed to get a deck with deck_id = {deck_id}:", exc_info=True
            )
            raise
        else:
            if not deck:
                raise DeckNotFoundException()

            permission = DeckViewPermission(current_user=self.user, deck=deck)
            permission.check_permissions()

            return deck

    async def get_all(self, *, filter: DecksFilter) -> List[Deck]:
        """Get all decks with provided conditions and check permissions

        Raises:
            NotEnoughPermissionsException: if a user didn't have enough permissions to view
        """
        try:
            async with self.uow:
                decks = await self.uow.decks.get_all(filter=filter)
        except SQLAlchemyError:
            logger.error(f"Failed to get decks with filter = {filter}:", exc_info=True)
            raise
        else:
            permission = DecksViewPermission(
                current_user=self.user,
                provided_visibility=filter.visibility,
                provided_user_id=filter.user_id,
            )
            permission.check_permissions()

            return decks

    async def get_by(self, *, filter: DeckFilter) -> Optional[Deck]:
        """Get a deck by provided filter and check permissions

        Raises:
            NotEnoughPermissionsException: if a user didn't have enough permissions to view
        """
        try:
            async with self.uow:
                deck = await self.uow.decks.get_by(filter=filter)
        except SQLAlchemyError:
            logger.error(f"Failed to get a deck with filter = {filter}:", exc_info=True)
            raise
        else:
            if not deck:
                return None

            permission = DeckViewPermission(current_user=self.user, deck=deck)
            permission.check_permissions()

            return deck

    async def update(self, *, deck_id: UUID4, data: DeckUpdate) -> Deck:
        """Update a deck by its ID with the provided data and check permissions

        Raises:
            NotEnoughPermissionsException: if a user isn't an admin or owner
        """
        try:
            async with self.uow:
                deck = await self.get(deck_id=deck_id)

                permission = OwnerPermission(current_user=self.user, instance=deck)
                permission.check_permissions()

                if not data.are_new_column_values_provided(deck):
                    return deck

                update_data = data.model_dump(exclude_none=True)
                updated_deck: Deck = await self.uow.decks.update(
                    obj=deck, data=update_data
                )

                await self.uow.commit()
        except SQLAlchemyError:
            logger.error(
                f"Failed to update a deck with deck_id = {deck_id} and data = {data}:",
                exc_info=True,
            )
            raise
        else:
            return updated_deck

    async def delete(self, *, deck_id: UUID4) -> None:
        """Delete a deck by its id

        Raises:
            NotEnoughPermissionsException: if a user isn't an admin or owner
        """
        try:
            async with self.uow:
                deck = await self.uow.decks.get(id=deck_id)
                if deck:
                    permission = OwnerPermission(current_user=self.user, instance=deck)
                    permission.check_permissions()

                    await self.uow.decks.delete(obj_id=deck_id)
                    await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to delete a deck with deck_id = {deck_id}:", exc_info=True
            )
            raise exc
