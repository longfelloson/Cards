from typing import List, Optional

from cache.keys import Key
from cache.core import storage
from decks.exceptions import DeckAlreadyExistsException, DeckNotFoundException
from decks.models import Deck
from decks.schemas import DeckCreate, DeckFilter, DecksFilter, DeckUpdate
from pydantic import UUID4
from service import AbstractService
from unit_of_work import UnitOfWork


class DeckService(AbstractService):
    def __init__(self, *, storage, cache_keys):
        self.storage = storage
        self.cache_keys = cache_keys

    async def create(
        self,
        *,
        data: DeckCreate,
        user_id: UUID4,
        uow: UnitOfWork,
    ) -> Deck:
        """Create a deck with provided data"""
        async with uow:
            deck_filter = DeckFilter(name=data.name)
            deck = await self.get_by(filter=deck_filter, uow=uow)
            if deck:
                raise DeckAlreadyExistsException()

            deck: Deck = await uow.decks.create(data=data, user_id=user_id)

            await uow.commit()
            await self.clear_deck_related_cache(deck.id)

            return deck

    async def get(
        self,
        *,
        deck_id: UUID4,
        uow: UnitOfWork,
    ) -> Optional[Deck]:
        """Get a card with provided ID"""
        async with uow:
            deck = await uow.decks.get(id=deck_id)
            if not deck:
                raise DeckNotFoundException()
            return deck

    async def get_all(
        self,
        *,
        filter: DecksFilter,
        user_id: UUID4,
        uow: UnitOfWork,
    ) -> List[Deck]:
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

            if not data.are_new_column_values_provided(deck):
                return deck

            update_data = data.model_dump(exclude_none=True)
            updated_deck: Deck = await uow.decks.update(obj=deck, data=update_data)

            await uow.commit()
            await self.clear_deck_related_cache(deck.id)

            return updated_deck

    async def delete(self, *, deck_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a deck by its id"""
        async with uow:
            await uow.decks.delete(obj_id=deck_id)
            await uow.commit()
            await self.clear_deck_related_cache(deck_id)

    async def clear_deck_related_cache(self, deck_id: UUID4) -> None:
        """Delete a deck's related cache (deck:deck_id, decks:)"""
        await self.storage.clear_cache_by_keys(
            self.cache_keys.deck(deck_id), self.cache_keys.decks()
        )


decks_service = DeckService(storage=storage, cache_keys=Key)
