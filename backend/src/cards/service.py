from typing import Optional

from pydantic import UUID4
from sqlalchemy.exc import SQLAlchemyError

from auth.permissions.core import OwnerPermission
from constants import (
    CREATE_ERROR_LOG,
    DELETE_ERROR_LOG,
    GET_ERROR_LOG,
    GET_ALL_ERROR_LOG,
    GET_BY_ERROR_LOG,
    UPDATE_ERROR_LOG,
)
from cards.permissions import CardViewPermission, CardsViewPermission
from logger import logger
from cards.exceptions import CardAlreadyExistsException, CardNotFoundException
from cards.models import Card
from cards.review import get_card_review
from cards.schemas import CardCreate, CardFilter, CardsFilter, CardUpdate
from service import AbstractService


class CardsService(AbstractService):
    def __init__(self, *, storage, uow, user):
        self.user = user
        self.uow = uow
        self.storage = storage

    async def create(self, *, data: CardCreate) -> Card:
        """Create a card with provided data"""
        try:
            async with self.uow:
                card_filter = CardFilter(face=data.face, user_id=self.user.id)
                card = await self.uow.cards.get_by(filter=card_filter)
                if card:
                    raise CardAlreadyExistsException()

                card = await self.uow.cards.create(data=data, user_id=self.user.id)

                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                CREATE_ERROR_LOG.format(
                    object=card or "card", user=self.user, data=data
                ),
                exc_info=True,
            )
            raise exc
        else:
            return card

    async def get(
        self,
        *,
        card_id: UUID4,
        check_permissions: bool = True,
        raise_error: bool = True,
    ) -> Card:
        """Get a card by its id"""
        try:
            async with self.uow:
                card = await self.uow.cards.get(id=card_id)

                if not card and raise_error:
                    raise CardNotFoundException()

                if card is not None and check_permissions:
                    permission = CardViewPermission(current_user=self.user, card=card)
                    permission.check_permissions()
        except SQLAlchemyError as exc:
            logger.error(
                GET_ERROR_LOG.format(object=card or "card", object_id=card_id),
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
                if card:
                    permission = CardViewPermission(current_user=self.user, card=card)
                    permission.check_permissions()
        except SQLAlchemyError as exc:
            logger.error(
                GET_BY_ERROR_LOG.format(object=card or "card", filter=filter),
                exc_info=True,
            )
            raise exc
        else:
            return card

    async def get_all(self, *, filter: CardsFilter) -> list[Card]:
        """Get cards by provided options"""
        try:
            permission = CardsViewPermission(
                current_user=self.user,
                provided_visibility=filter.visibility,
                provided_user_id=filter.user_id,
            )
            permission.check_permissions()

            async with self.uow:
                cards = await self.uow.cards.get_all(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(
                GET_ALL_ERROR_LOG.format(object="cards", filter=filter),
                exc_info=True,
            )
            raise exc
        else:
            return cards

    async def update(self, *, card_id: UUID4, data: CardUpdate) -> Card:
        """Update a card by its ID with the provided data"""
        try:
            async with self.uow:
                card = await self.get(card_id=card_id, check_permissions=False)

                if card:
                    permission = OwnerPermission(current_user=self.user, instance=card)
                    permission.check_permissions()

                update_data = data.model_dump(exclude_none=True)

                if data.last_memorization_level:
                    card_review = get_card_review(data.last_memorization_level, card)
                    update_data.update(card_review.model_dump(exclude_none=True))

                updated_card = await self.uow.cards.update(obj=card, data=update_data)

                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                UPDATE_ERROR_LOG.format(
                    object=card or "card", object_id=card_id, data=data
                ),
                exc_info=True,
            )
            raise exc
        else:
            return updated_card

    async def delete(self, *, card_id: UUID4) -> None:
        """Delete a card by its id"""
        try:
            async with self.uow:
                card = await self.get(
                    card_id=card_id, check_permissions=False, raise_error=False
                )
                if card:
                    permission = OwnerPermission(current_user=self.user, instance=card)
                    permission.check_permissions()

                    await self.uow.cards.delete(obj_id=card_id)
                    await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                DELETE_ERROR_LOG.format(object=card or "card", object_id=card_id),
                exc_info=True,
            )
            raise exc
