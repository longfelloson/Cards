from typing import Optional

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


class CollectionService(AbstractService):
    async def create(self, *, data: CollectionCreate, uow: UnitOfWork) -> Collection:
        """Create a collection with provided data"""
        async with uow:
            collection_filter = CollectionFilter(name=data.name)
            collection = await self.get_by(filter=collection_filter)
            if collection:
                raise CollectionAlreadyExistsException()
            collection = await uow.collections.create(data=data)
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
        self, *, filter: CollectionsFilter, user_id: UUID4, uow: UnitOfWork
    ) -> list[Collection]:
        """Get collections by provided conditions"""
        filter.user_id = user_id
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
            await uow.session.refresh(updated_collection)

            return updated_collection

    async def delete(self, *, collection_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a collection by its id"""
        async with uow:
            await uow.collections.delete(onj_id=collection_id)


service = CollectionService()
