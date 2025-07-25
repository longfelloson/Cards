from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Optional

from pydantic import UUID4

from auth.permissions.exceptions import NotEnoughPermissionsException
from auth.rbac.enums import Role
from enums import Visibility
from users.models import User


@dataclass(kw_only=True)
class BasePermission(ABC):
    """Base permission class that provides base functionality"""
    current_user: User

    def check_permissions(self) -> None | bool:
        if self.current_user.role == Role.ADMIN:
            return True

        if not self.has_required_permissions():
            raise NotEnoughPermissionsException(permission=self)

    @abstractmethod
    def has_required_permissions(self) -> bool:
        raise NotImplementedError()

    def __str__(self):
        return f"permission {self.__class__.__name__}"


@dataclass(kw_only=True)
class OwnerPermission(BasePermission):
    """Check if a user is the owner of an instance"""

    instance: object

    def has_required_permissions(self) -> bool:
        return self.instance.user_id == self.current_user.id


@dataclass(kw_only=True)
class UserMatchPermission(BasePermission):
    """Check if user provided his own user id"""
    
    provided_user_id: Optional[UUID4]

    def has_required_permissions(self) -> bool:
        return self.provided_user_id == self.current_user.id


@dataclass(kw_only=True)
class VisibilityPermission(BasePermission):
    """Check if user requests either his own resource or required visibility"""
    
    provided_visibility: Visibility = None
    required_visibility: Visibility = Visibility.visible
    instance: object = None

    def has_required_permissions(self) -> bool:
        if self.instance:
            if not hasattr(self.instance, "visibility"):
                raise AttributeError(
                    f"{self.instance} must have the visibility attribute!"
                )
            return self.instance.visibility == self.required_visibility

        if not self.provided_visibility:
            return True

        return self.provided_visibility == self.required_visibility
