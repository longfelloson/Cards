from typing import Optional

from pydantic import UUID4

from service import AbstractService
from unit_of_work import UnitOfWork
from decks.exceptions import DeckAlreadyExists, DeckNotFound
from decks.models import Deck
from decks.schemas import DeckCreate, DeckFilter, DeckUpdate, DecksFilter


class DeckService(AbstractService):
    async def create(
        self,
        *,
        data: DeckCreate,
        user_id: UUID4,
        uow: UnitOfWork,
    ) -> Deck:
        """Creates a card with provided data"""
        async with uow:
            deck_filter = DeckFilter(name=data.name)
            deck = await self.get_by(filter=deck_filter, uow=uow)
            if deck:
                raise DeckAlreadyExists()

            deck = await uow.decks.create(data=data, user_id=user_id)
            return deck

    async def get(
        self,
        *,
        deck_id: UUID4,
        uow: UnitOfWork,
    ) -> Optional[Deck]:
        """Gets a card with provided ID"""
        async with uow:
            deck = await uow.decks.get(id=deck_id)
            if not deck:
                raise DeckNotFound()
            return deck

    async def get_all(
        self,
        *,
        filter: DecksFilter,
        user_id: UUID4,
        uow: UnitOfWork,
    ) -> list[Deck]:
        """Get all decks with provided conditions"""
        filter.user_id = user_id
        async with uow:
            decks = await uow.decks.get_all(filter=filter)
            return decks

    async def get_by(self, *, filter: DeckFilter, uow: UnitOfWork) -> Optional[Deck]:
        """Get a deck by provided filter"""
        async with uow:
            deck = await uow.decks.get_by(filter=filter)
            return deck

    async def update(
        self,
        *,
        deck_id: UUID4,
        data: DeckUpdate,
        uow: UnitOfWork,
    ) -> Deck:
        """Update a deck by its ID with the provided data."""
        async with uow:
            deck = await self.get(deck_id=deck_id, uow=uow)
            update_data = data.model_dump(exclude_none=True)
            updated_deck = await uow.decks.update(obj=deck, data=update_data)
            return updated_deck

    async def delete(self, *, deck_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a deck by its id"""
        async with uow:
            deck = await self.get(deck_id=deck_id, uow=uow)
            await uow.decks.delete(obj=deck)


service = DeckService()
