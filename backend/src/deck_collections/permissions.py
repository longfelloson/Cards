from fastapi import Request

from auth.permissions import (
    BasePermission,
    OwnerPermission,
    VisibilityPermission,
    any_permission,
)
from deck_collections.service import collections_service


class CollectionOwnerPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        collection_id = request.path_params["collection_id"]
        collection = await collections_service.get(
            collection_id=collection_id, uow=request.state.uow
        )

        return collection.user_id == request.user.id


class CollectionViewPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        """
        Check if user owns a collection or requires visible one
        """
        collection_id = request.path_params["collection_id"]
        collection = await collections_service.get(
            collection_id=collection_id, uow=request.state.uow
        )

        has_permission = await any_permission(
            permissions=[
                OwnerPermission(instance=collection),
                VisibilityPermission(instance=collection),
            ],
            request=request,
        )
        return has_permission
