from datetime import datetime

from cards.models import Card
from cards.schemas import CardsFilter
from repository import SQLAlchemyRepository
from sqlalchemy import and_, or_, select


class CardsRepository(SQLAlchemyRepository):
    model = Card

    async def get_all(self, filter: CardsFilter) -> list[Card]:
        """Get cards by filter"""
        stmt = select(self.model)
        conditions = [*filter.get_conditions(self.model)]

        if filter.query:
            conditions.append(self.model.face.ilike(filter.query))

        if filter.to_study:
            conditions.append(
                or_(
                    self.model.next_review_at <= datetime.now(),
                    self.model.next_review_at.is_(None),
                )
            )

        stmt = stmt.where(and_(*conditions))
        stmt = stmt.offset(filter.offset).limit(filter.limit)

        cards = await self.session.execute(stmt)
        return cards.scalars().all()
