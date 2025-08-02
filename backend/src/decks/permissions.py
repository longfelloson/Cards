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
from decks.models import Deck
from enums import Visibility


@dataclass(kw_only=True)
class DeckViewPermission(BasePermission):
    """
    Check if user owns a deck or requires visible one
    """

    deck: Deck

    def has_required_permissions(self) -> bool:
        has_permission = any_permission(
            OwnerPermission(instance=self.deck, current_user=self.current_user),
            VisibilityPermission(
                current_user=self.current_user, instance=self.deck
            ),
        )
        return has_permission


@dataclass(kw_only=True)
class DecksViewPermission(BasePermission):
    """
    Check if user requests its own decks or not hidden ones
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
