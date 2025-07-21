from abc import ABC, abstractmethod

from dataclasses import dataclass
from fastapi import HTTPException, Request

from auth.rbac.exceptions import ResourceNotFound
from auth.rbac.enums import Role
from enums import Visibility


async def all_permissions(permissions: list, request: Request) -> bool:
    for permission in permissions:
        try:
            await permission(request=request)
        except HTTPException:
            return False

    return True


async def any_permission(permissions: list, request: Request) -> bool:
    for permission in permissions:
        try:
            await permission(request=request)
        except HTTPException:
            return False
        else:
            return True


class BasePermission(ABC):
    async def __call__(self, request: Request):
        if request.user.role == Role.ADMIN:
            return True

        if not await self.has_required_permissions(request):
            raise ResourceNotFound()

    @abstractmethod
    async def has_required_permissions(self, request: Request) -> bool:
        raise NotImplementedError()


@dataclass
class OwnerPermission(BasePermission):
    instance: object

    async def has_required_permissions(self, request: Request) -> bool:
        return self.instance.user_id == request.user.id


class UserMatchPermission(BasePermission):
    async def has_required_permissions(self, request):
        user_id = request.query_params.get("user_id")
        return user_id and user_id == request.user.id


@dataclass
class VisibilityPermission(BasePermission):
    required_visibility: Visibility = Visibility.visible
    instance: object = None

    async def has_required_permissions(self, request: Request) -> bool:
        """
        Check if user requests either his own resource or required visibility
        """
        provided_visibility = request.query_params.get("visibility")

        if self.instance:
            if not hasattr(self.instance, "visibility"):
                raise AttributeError(
                    f"{self.instance} must have the visibility attribute!"
                )
            return self.instance.visibility == self.required_visibility

        if not provided_visibility:
            return True

        return provided_visibility == self.required_visibility
