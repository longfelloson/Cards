from deck_collections.models import Collection, CollectionDeck
from deck_collections.schemas import CollectionCreate
from pydantic import UUID4
from repository import SQLAlchemyRepository
from sqlalchemy import and_, delete as delete_


class CollectionsRepository(SQLAlchemyRepository):
    model = Collection

    async def create(self, *, data: CollectionCreate, user_id: UUID4) -> Collection:
        """Create a collection and its cards with provided data"""
        collection = self.model(name=data.name, user_id=user_id)

        self.session.add(collection)
        await self.session.flush()

        return collection


class CollectionDecksRepository(SQLAlchemyRepository):
    model = CollectionDeck

    async def create(self, collection_id: UUID4, deck_ids: list[UUID4]) -> None:
        for deck_id in deck_ids:
            collection_deck = self.model(collection_id=collection_id, deck_id=deck_id)
            self.session.add(collection_deck)

        await self.session.flush()

    async def delete(self, deck_id: UUID4, collection_id: UUID4) -> None:
        await self.session.execute(
            delete_(self.model).where(
                and_(
                    self.model.collection_id == collection_id,
                    self.model.deck_id == deck_id,
                )
            )
        )
