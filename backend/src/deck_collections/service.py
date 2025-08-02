from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from pydantic import UUID4

from auth.permissions.core import OwnerPermission
from constants import (
    CREATE_ERROR_LOG,
    DELETE_ERROR_LOG,
    GET_ALL_ERROR_LOG,
    GET_BY_ERROR_LOG,
    GET_ERROR_LOG,
    UPDATE_ERROR_LOG,
)
from deck_collections.exceptions import (
    CollectionAlreadyExistsException,
    CollectionNotFoundException,
)
from deck_collections.models import Collection
from deck_collections.permissions import (
    CollectionViewPermission,
    CollectionsViewPermission,
)
from deck_collections.schemas import (
    CollectionCreate,
    CollectionFilter,
    CollectionsFilter,
    CollectionUpdate,
)
from logger import logger
from service import AbstractService


class CollectionsService(AbstractService):
    def __init__(self, *, storage, uow, user):
        self.storage = storage
        self.uow = uow
        self.user = user

    async def create(self, *, data: CollectionCreate) -> Collection:
        """Create a collection with provided data"""
        try:
            async with self.uow:
                collection_filter = CollectionFilter(name=data.name)
                collection = await self.uow.collections.get_by(filter=collection_filter)

                if collection:
                    raise CollectionAlreadyExistsException()

                collection = await self.uow.collections.create(
                    data=data, user_id=self.user.id
                )

                await self.uow.collection_decks.create(collection.id, data.deck_ids)
                await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                CREATE_ERROR_LOG.format(
                    object=collection or "collection", user=self.user, data=data
                ),
                exc_info=True,
            )
            raise exc
        else:
            return collection

    async def get(
        self,
        *,
        collection_id: UUID4,
        raise_error: bool = True,
        check_permissions: bool = True,
    ) -> Collection:
        """Get a collection by its id.

        Args:
            raise_error (bool, optional): if you need to raise an error
            if a collection was not found
        """
        try:
            async with self.uow:
                collection = await self.uow.collections.get(id=collection_id)

                if not collection and raise_error:
                    raise CollectionNotFoundException()

                if collection is not None and check_permissions:
                    permission = CollectionViewPermission(
                        current_user=self.user, collection=collection
                    )
                    permission.check_permissions()
        except SQLAlchemyError as exc:
            logger.error(
                GET_ERROR_LOG.format(
                    object=collection or "collection", object_id=collection_id
                ),
                exc_info=True,
            )
            raise exc
        else:
            return collection

    async def get_by(self, *, filter: CollectionFilter) -> Optional[Collection]:
        """Get a collection by filter"""
        try:
            async with self.uow:
                collection = await self.uow.collections.get_by(filter=filter)

                if collection:
                    permission = CollectionViewPermission(
                        current_user=self.user, collection=collection
                    )
                    permission.check_permissions()
        except SQLAlchemyError as exc:
            logger.error(
                GET_BY_ERROR_LOG.format(
                    object=collection or "collection", filter=filter
                ),
                exc_info=True,
            )
            raise exc
        else:
            return collection

    async def get_all(self, *, filter: CollectionsFilter) -> list[Collection]:
        """Get collections by provided conditions"""
        try:
            async with self.uow:
                permission = CollectionsViewPermission(
                    current_user=self.user,
                    provided_visibility=filter.visibility,
                    provided_user_id=filter.user_id,
                )
                permission.check_permissions()

                collections = await self.uow.collections.get_all(filter=filter)
        except SQLAlchemyError as exc:
            logger.error(
                GET_ALL_ERROR_LOG.format(object="collections", filter=filter),
                exc_info=True,
            )
            raise exc
        else:
            return collections

    async def update(
        self, *, collection_id: UUID4, data: CollectionUpdate
    ) -> Collection:
        """Update a collection with provided data"""
        try:
            async with self.uow:
                collection = await self.get(
                    collection_id=collection_id, check_permissions=False
                )
                if collection:
                    permission = OwnerPermission(
                        current_user=self.user, instance=collection
                    )
                    permission.check_permissions()

                    update_data = data.model_dump(exclude_unset=True)

                    decks_ids = update_data.pop("decks_ids", None)
                    updated_collection = await self.uow.collections.update(
                        obj=collection, data=update_data
                    )

                    if decks_ids is not None:
                        await self.collection_decks.delete(collection_id=collection_id)
                        await self.uow.collection_decks.create(
                            collection_id=collection_id, decks_ids=decks_ids
                        )

                    await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                UPDATE_ERROR_LOG.format(
                    object=collection or "collection", user=self.user, data=data
                ),
                exc_info=True,
            )
            raise exc
        else:
            return updated_collection

    async def delete(self, *, collection_id: UUID4) -> None:
        """Delete a collection by its id"""
        try:
            async with self.uow:
                collection = await self.get(
                    collection_id=collection_id,
                    raise_error=False,
                    check_permissions=False,
                )
                if collection:
                    OwnerPermission(current_user=self.user, instance=collection)

                    await self.uow.collections.delete(obj_id=collection_id)
                    await self.uow.commit()
        except SQLAlchemyError as exc:
            logger.error(
                DELETE_ERROR_LOG.format(
                    object=collection or "collection", object_id=collection_id
                ),
                exc_info=True,
            )
            raise exc
