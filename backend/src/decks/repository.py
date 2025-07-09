from datetime import datetime

from cards.models import Card
from deck_collections.models import CollectionDeck
from decks.models import Deck
from decks.schemas import DecksFilter
from pydantic import UUID4
from repository import SQLAlchemyRepository
from sqlalchemy import and_, or_, select


class DecksRepository(SQLAlchemyRepository):
    model = Deck

    async def get_collection_decks(self, *, collection_id: UUID4) -> list[Deck]:
        """Get decks with collection id"""
        collection_decks = await self.session.execute(
            select(CollectionDeck).where(CollectionDeck.collection_id == collection_id)
        )
        return collection_decks.scalars().all()

    async def get_all(self, *, filter: DecksFilter) -> list[Deck]:
        """Get decks by provided conditions"""
        stmt = select(self.model)

        if filter.to_study:
            stmt = (
                stmt.join(self.model.cards)
                .filter(
                    or_(
                        Card.next_review_at <= datetime.now(),
                        Card.next_review_at.is_(None),
                    )
                )
                .distinct()
            )

        conditions = [*filter.get_conditions(self.model)]

        if filter.query:
            conditions.append(self.model.name.ilike(f"%{filter.query}%"))

        stmt = stmt.where(and_(*conditions))
        stmt = stmt.offset(filter.offset).limit(filter.limit)

        decks = await self.session.execute(stmt)
        return decks.scalars().all()
