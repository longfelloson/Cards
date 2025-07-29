from dataclasses import dataclass
from typing import Optional

from pydantic import UUID4

from auth.permissions.core import (
    BasePermission,
    OwnerPermission,
    UserMatchPermission,
    VisibilityPermission,
)
from auth.permissions.utils import any_permission
from deck_collections.models import Collection
from enums import Visibility


@dataclass(kw_only=True)
class CollectionViewPermission(BasePermission):
    """
    Check if user owns a collection or requires visible one
    """

    collection: Collection

    def has_required_permissions(self) -> bool:
        has_permission = any_permission(
            OwnerPermission(instance=self.collection, current_user=self.current_user),
            VisibilityPermission(
                current_user=self.current_user, instance=self.collection
            ),
        )
        return has_permission


@dataclass(kw_only=True)
class CollectionsViewPermission(BasePermission):
    """
    Check if user requires its own collections or not hidden ones
    """

    provided_visibility: Visibility
    provided_user_id: Optional[UUID4]

    def has_required_permissions(self) -> bool:
        has_permission = any_permission(
            UserMatchPermission(
                current_user=self.current_user, provided_user_id=self.provided_user_id
            ),
            VisibilityPermission(
                current_user=self.current_user,
                provided_visibility=self.provided_visibility,
            ),
        )
        return has_permission
