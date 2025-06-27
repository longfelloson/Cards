from pydantic import UUID4
from deck_collections.schemas import CollectionCreate
from deck_collections.models import Collection, CollectionDeck
from repository import SQLAlchemyRepository
from sqlalchemy import delete as delete_


class CollectionsRepository(SQLAlchemyRepository):
    model = Collection

    async def create(self, *, data: CollectionCreate) -> Collection:
        """Create a collection and its cards with provided data"""
        collection = Collection(name=data.name)

        self.session.add(collection)
        await self.session.flush()

        for deck_id in data.decks_ids:
            deck = CollectionDeck(collection_id=collection.id, id=deck_id)
            self.session.add(deck)

        await self.session.commit()
        await self.session.refresh(collection)

        return collection


class CollectionDecksRepository(SQLAlchemyRepository):
    model = CollectionDeck

    async def create(self, collection_id: UUID4, decks_ids: list[UUID4]) -> None:
        for deck_id in decks_ids:
            collection_deck = CollectionDeck(
                collection_id=collection_id, deck_id=deck_id
            )
            self.session.add(collection_deck)
        await self.session.flush()
        await self.session.commit()

    async def delete(self, collection_id: UUID4) -> None:
        await self.session.execute(
            delete_(CollectionDeck).where(CollectionDeck.collection_id == collection_id)
        )
        await self.session.flush()
        await self.session.commit()
