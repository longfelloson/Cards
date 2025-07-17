from fastapi import Request

from auth.permissions import BasePermission
from deck_collections.service import collections_service


class CollectionOwnerPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        collection_id = request.path_params["collection_id"]
        collection = await collections_service.get(
            collection_id=collection_id, uow=request.state.uow
        )

        return collection.user_id == request.user.id
