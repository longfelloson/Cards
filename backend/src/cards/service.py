from typing import Optional

from cards.exceptions import CardAlreadyExistsException, CardNotFoundException
from cards.models import Card
from cards.review import get_card_review
from cards.schemas import CardCreate, CardFilter, CardsFilter, CardUpdate
from pydantic import UUID4
from service import AbstractService
from unit_of_work import UnitOfWork


class CardsService(AbstractService):
    async def create(
        self,
        *,
        data: CardCreate,
        user_id: UUID4,
        uow: UnitOfWork,
    ) -> Card:
        """Create a card with provided data"""
        async with uow:
            card_filter = CardFilter(face=data.face, user_id=user_id)
            card = await uow.cards.get_by(filter=card_filter)
            if card:
                raise CardAlreadyExistsException()
            card = await uow.cards.create(data=data, user_id=user_id)
            return card

    async def get(
        self, *, card_id: UUID4, uow: UnitOfWork, raise_error: bool = True
    ) -> Card:
        """Get a card by its id"""
        async with uow:
            card = await uow.cards.get(id=card_id)
            if not card and raise_error:
                raise CardNotFoundException()
            return card

    async def get_by(self, *, filter: CardFilter, uow: UnitOfWork) -> Optional[Card]:
        """Get a card by filter"""
        async with uow:
            card = await uow.cards.get_by(filter=filter)
            return card

    async def get_all(
        self, filter: CardsFilter, user_id: UUID4, uow: UnitOfWork
    ) -> list[Card]:
        """Get cards by provided options"""
        async with uow:
            filter.user_id = user_id
            cards = await uow.cards.get_all(filter=filter)
            return cards

    async def update(
        self,
        *,
        card_id: UUID4,
        data: CardUpdate,
        uow: UnitOfWork,
    ) -> Card:
        """Update a card by its ID with the provided data"""
        async with uow:
            card = await self.get(card_id=card_id, uow=uow)
            update_data = data.model_dump(exclude_none=True)

            if data.last_memorization_level:
                card_review = get_card_review(data.last_memorization_level, card)
                update_data.update(card_review.model_dump(exclude_none=True))

            updated_card = await uow.cards.update(obj=card, data=update_data)
            return updated_card

    async def delete(self, *, card_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a card by its id"""
        async with uow:
            await uow.cards.delete(obj_id=card_id)


service = CardsService()
