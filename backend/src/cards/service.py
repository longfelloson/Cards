from typing import Optional

from pydantic import UUID4
from sqlalchemy.exc import SQLAlchemyError

from logger import logger
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
        try:
            async with self.uow:
                card_filter = CardFilter(face=data.face, user_id=user_id)
                card = await self.uow.cards.get_by(filter=card_filter)

                if card:
                    raise CardAlreadyExistsException()

                card = await self.uow.cards.create(data=data, user_id=user_id)

                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to create card for user_id = {user_id} and data = {data}:",
                exc_info=True,
            )
            raise exc
        else:
            return card

    async def get(self, *, card_id: UUID4, raise_error: bool = True) -> Card:
        """Get a card by its id"""
        try:
            async with self.uow:
                card = await self.uow.cards.get(id=card_id)
                if not card and raise_error:
                    raise CardNotFoundException()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to get a card with card_id = {card_id}:",
                exc_info=True,
            )
            raise exc
        else:
            return card

    async def get_by(self, *, filter: CardFilter) -> Optional[Card]:
        """Get a card by filter"""
        try:
            async with self.uow:
                card = await self.uow.cards.get_by(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(f"Failed to get a card with filter = {filter}:", exc_info=True)
            raise exc
        else:
            return card

    async def get_all(self, filter: CardsFilter) -> list[Card]:
        """Get cards by provided options"""
        try:
            async with self.uow:
                cards = await self.uow.cards.get_all(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(f"Failed to get cards with filter = {filter}:", exc_info=True)
            raise exc
        else:
            return cards

    async def update(
        self,
        *,
        card_id: UUID4,
        data: CardUpdate,
    ) -> Card:
        """Update a card by its ID with the provided data"""
        try:
            async with self.uow:
                card = await self.get(card_id=card_id)
                update_data = data.model_dump(exclude_none=True)

                if data.last_memorization_level:
                    card_review = get_card_review(data.last_memorization_level, card)
                    update_data.update(card_review.model_dump(exclude_none=True))

                updated_card = await self.uow.cards.update(obj=card, data=update_data)

                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to update a card with card_id = {card_id} and data = {data}:",
                exc_info=True,
            )
            raise exc
        else:
            return updated_card

    async def delete(self, *, card_id: UUID4) -> None:
        """Delete a card by its id"""
        try:
            async with self.uow:
                await self.uow.cards.delete(obj_id=card_id)
                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to delete a card with card_id = {card_id}:", exc_info=True
            )
            raise exc
