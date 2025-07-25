from typing import Optional

from cache.keys import Key
from cache.core import storage
from deck_collections.exceptions import (
    CollectionAlreadyExistsException,
    CollectionNotFoundException,
)
from deck_collections.models import Collection
from deck_collections.schemas import (
    CollectionCreate,
    CollectionFilter,
    CollectionsFilter,
    CollectionUpdate,
)
from pydantic import UUID4
from service import AbstractService
from unit_of_work import UnitOfWork


class CollectionsService(AbstractService):
    def __init__(self, *, storage, cache_keys):
        self.storage = storage
        self.cache_keys = cache_keys

    async def create(
        self, *, data: CollectionCreate, user_id: UUID4, uow: UnitOfWork
    ) -> Collection:
        """Create a collection with provided data"""
        async with uow:
            collection_filter = CollectionFilter(name=data.name)
            collection = await self.get_by(filter=collection_filter, uow=uow)

            if collection:
                raise CollectionAlreadyExistsException()

            collection = await uow.collections.create(data=data, user_id=user_id)
            await uow.collection_decks.create(collection.id, data.deck_ids)

            await uow.commit()
            await self.clear_collection_related_cache(collection.id)

            return collection

    async def get(self, *, collection_id: UUID4, uow: UnitOfWork) -> Collection:
        """Get a collection by its id"""
        async with uow:
            collection = await uow.collections.get(id=collection_id)
            if not collection:
                raise CollectionNotFoundException()
            return collection

    async def get_by(
        self, *, filter: CollectionFilter, uow: UnitOfWork
    ) -> Optional[Collection]:
        """Get a collection by filter"""
        async with uow:
            collection = await uow.collections.get_by(filter=filter)
            return collection

    async def get_all(
        self,
        *,
        filter: CollectionsFilter,
        uow: UnitOfWork,
    ) -> list[Collection]:
        """Get collections by provided conditions"""
        async with uow:
            collections = await uow.collections.get_all(filter=filter)
            return collections

    async def update(
        self, *, collection_id: UUID4, data: CollectionUpdate, uow: UnitOfWork
    ) -> Collection:
        async with uow:
            collection = await self.get(collection_id=collection_id, uow=uow)
            update_data = data.model_dump(exclude_unset=True)

            decks_ids = update_data.pop("decks_ids", None)
            updated_collection = await uow.collections.update(
                obj=collection, data=update_data
            )

            if decks_ids is not None:
                await uow.collection_decks.delete(collection_id=collection_id)
                await uow.collection_decks.create(
                    collection_id=collection_id, decks_ids=decks_ids
                )

            await uow.commit()
            await self.clear_collection_related_cache(collection_id)

            return updated_collection

    async def delete(self, *, collection_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a collection by its id"""
        async with uow:
            await uow.collections.delete(obj_id=collection_id)
            await uow.commit()
            await self.clear_collection_related_cache(collection_id)

    async def clear_collection_related_cache(self, collection_id: UUID4) -> None:
        await self.storage.clear_cache_by_keys(
            self.cache_keys.collection(collection_id), self.cache_keys.collections()
        )


collections_service = CollectionsService(storage=storage, cache_keys=Key)
