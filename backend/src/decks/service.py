from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from pydantic import UUID4

from logger import logger
from decks.exceptions import DeckAlreadyExistsException, DeckNotFoundException
from decks.models import Deck
from decks.schemas import DeckCreate, DeckFilter, DecksFilter, DeckUpdate
from service import AbstractService


class DeckService(AbstractService):
    def __init__(self, *, storage, uow):
        self.storage = storage
        self.uow = uow

    async def create(self, *, data: DeckCreate, user_id: UUID4) -> Deck:
        """Create a deck with provided data"""
        try:
            async with self.uow:
                deck_filter = DeckFilter(name=data.name)
                deck = await self.get_by(filter=deck_filter)
                if deck:
                    raise DeckAlreadyExistsException()

                deck: Deck = await self.uow.decks.create(data=data, user_id=user_id)

                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to create a deck with user_id = {user_id} and data = {data}",
                exc_info=True,
            )
            raise exc
        else:
            return deck

    async def get(self, *, deck_id: UUID4) -> Optional[Deck]:
        """Get a card with provided ID"""
        try:
            async with self.uow:
                deck = await self.uow.decks.get(id=deck_id)
                if not deck:
                    raise DeckNotFoundException()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to get a deck with deck_id = {deck_id}:", exc_info=True
            )
            raise exc
        else:
            return deck

    async def get_all(self, *, filter: DecksFilter) -> List[Deck]:
        """Get all decks with provided conditions"""
        try:
            async with self.uow:
                decks = await self.uow.decks.get_all(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(f"Failed to get decks with filter = {filter}:", exc_info=True)
            raise exc
        else:
            return decks

    async def get_by(self, *, filter: DeckFilter) -> Optional[Deck]:
        """Get a deck by provided filter"""
        try:
            async with self.uow:
                deck = await self.uow.decks.get_by(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(f"Failed to get a deck with filter = {filter}:", exc_info=True)
            raise exc
        else:
            return deck

    async def update(self, *, deck_id: UUID4, data: DeckUpdate) -> Deck:
        """Update a deck by its ID with the provided data"""
        try:
            async with self.uow:
                deck = await self.get(deck_id=deck_id)

                if not data.are_new_column_values_provided(deck):
                    return deck

                update_data = data.model_dump(exclude_none=True)
                updated_deck: Deck = await self.uow.decks.update(
                    obj=deck, data=update_data
                )

                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to update a deck with deck_id = {deck_id} and data = {data}:",
                exc_info=True,
            )
            raise exc
        else:
            return updated_deck

    async def delete(self, *, deck_id: UUID4) -> None:
        """Delete a deck by its id"""
        try:
            async with self.uow:
                await self.uow.decks.delete(obj_id=deck_id)
                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to delete a deck with deck_id = {deck_id}:", exc_info=True
            )
            raise exc
