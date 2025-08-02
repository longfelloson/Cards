from typing import Optional

from dataclasses import dataclass

from pydantic import UUID4

from auth.permissions.core import (
    BasePermission,
    OwnerPermission,
    UserMatchPermission,
    VisibilityPermission,
)
from auth.permissions.utils import any_permission
from cards.models import Card
from enums import Visibility


@dataclass(kw_only=True)
class CardViewPermission(BasePermission):
    """Check if user is an admin or owns the card"""

    card: Card

    def has_required_permissions(self) -> bool:
        has_permission = any_permission(
            OwnerPermission(current_user=self.current_user, instance=self.card),
            VisibilityPermission(current_user=self.current_user, instance=self.card),
        )
        return has_permission


@dataclass(kw_only=True)
class CardsViewPermission(BasePermission):
    """Check if user requires its own cards or not hidden cards"""

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
