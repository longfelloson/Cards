from typing import Optional

from pydantic import UUID4

from cards.exceptions import CardAlreadyExistsException, CardNotFoundException
from cards.models import Card
from cards.review import get_card_review
from cards.schemas import CardCreate, CardFilter, CardsFilter, CardUpdate
from service import AbstractService


class CardsService(AbstractService):
    def __init__(self, *, storage, uow):
        self.uow = uow
        self.storage = storage

    async def create(
        self,
        *,
        data: CardCreate,
        user_id: UUID4,
    ) -> Card:
        """Create a card with provided data"""
        async with self.uow:
            card_filter = CardFilter(face=data.face, user_id=user_id)
            card = await self.uow.cards.get_by(filter=card_filter)
            if card:
                raise CardAlreadyExistsException()
            card = await self.uow.cards.create(data=data, user_id=user_id)

            await self.uow.commit()
            await self.clear_card_related_cache(card.id)

            return card

    async def get(self, *, card_id: UUID4, raise_error: bool = True) -> Card:
        """Get a card by its id"""
        async with self.uow:
            card = await self.uow.cards.get(id=card_id)
            if not card and raise_error:
                raise CardNotFoundException()
            return card

    async def get_by(self, *, filter: CardFilter) -> Optional[Card]:
        """Get a card by filter"""
        async with self.uow:
            card = await self.uow.cards.get_by(filter=filter)
            return card

    async def get_all(self, filter: CardsFilter) -> list[Card]:
        """Get cards by provided options"""
        async with self.uow:
            cards = await self.uow.cards.get_all(filter=filter)
            return cards

    async def update(
        self,
        *,
        card_id: UUID4,
        data: CardUpdate,
    ) -> Card:
        """Update a card by its ID with the provided data"""
        async with self.uow:
            card = await self.get(card_id=card_id)
            update_data = data.model_dump(exclude_none=True)

            if data.last_memorization_level:
                card_review = get_card_review(data.last_memorization_level, card)
                update_data.update(card_review.model_dump(exclude_none=True))

            updated_card = await self.uow.cards.update(obj=card, data=update_data)

            await self.uow.commit()
            await self.clear_card_related_cache(card_id)

            return updated_card

    async def delete(self, *, card_id: UUID4) -> None:
        """Delete a card by its id"""
        async with self.uow:
            await self.uow.cards.delete(obj_id=card_id)
            await self.uow.commit()
            await self.clear_card_related_cache(card_id)

    async def clear_card_related_cache(self, card_id: UUID4) -> None:
        await self.storage.clear_cache_by_keys(
            self.storage.keys.card(card_id), self.storage.keys.cards()
        )
