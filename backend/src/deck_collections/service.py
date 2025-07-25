from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from pydantic import UUID4

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
from logger import logger
from service import AbstractService
from unit_of_work import UnitOfWork


class CollectionsService(AbstractService):
    def __init__(self, *, storage):
        self.storage = storage

    async def create(
        self, *, data: CollectionCreate, user_id: UUID4, uow: UnitOfWork
    ) -> Collection:
        """Create a collection with provided data"""
        try:
            async with uow:
                collection_filter = CollectionFilter(name=data.name)
                collection = await self.get_by(filter=collection_filter, uow=uow)

                if collection:
                    raise CollectionAlreadyExistsException()

                collection = await uow.collections.create(data=data, user_id=user_id)
                await uow.collection_decks.create(collection.id, data.deck_ids)

                await uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to create a collection with user_id = {user_id} and data = {data}",
                exc_info=True,
            )
            raise exc
        else:
            return collection

    async def get(self, *, collection_id: UUID4, uow: UnitOfWork) -> Collection:
        """Get a collection by its id"""
        try:
            async with uow:
                collection = await uow.collections.get(id=collection_id)
                if not collection:
                    raise CollectionNotFoundException()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to get a collection with collection_id = {collection_id}:",
                exc_info=True,
            )
            raise exc
        else:
            return collection

    async def get_by(
        self, *, filter: CollectionFilter, uow: UnitOfWork
    ) -> Optional[Collection]:
        """Get a collection by filter"""
        try:
            async with uow:
                collection = await uow.collections.get_by(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to get a collection with filter = {filter}:", exc_info=True
            )
            raise exc
        else:
            return collection

    async def get_all(
        self,
        *,
        filter: CollectionsFilter,
        uow: UnitOfWork,
    ) -> list[Collection]:
        """Get collections by provided conditions"""
        try:
            async with uow:
                collections = await uow.collections.get_all(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to get collections with filter = {filter}:", exc_info=True
            )
            raise exc
        else:
            return collections

    async def update(
        self, *, collection_id: UUID4, data: CollectionUpdate, uow: UnitOfWork
    ) -> Collection:
        """Update a collection with provided data"""
        try:
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
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to update a collection with collection_id = {collection_id} and data = {data}:",
                exc_info=True,
            )
            raise exc
        else:
            return updated_collection

    async def delete(self, *, collection_id: UUID4, uow: UnitOfWork) -> None:
        """Delete a collection by its id"""
        try:
            async with uow:
                await uow.collections.delete(obj_id=collection_id)
                await uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Failed to delete a collection with collection_id = {collection_id}",
                exc_info=True,
            )
            raise exc
