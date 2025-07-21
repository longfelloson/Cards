from abc import ABC, abstractmethod

from dataclasses import dataclass
from fastapi import HTTPException, Request

from auth.rbac.exceptions import ResourceNotFound
from auth.rbac.enums import Role
from backend.enums import Visibility


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
        user_id = request.query_params.get('user_id')
        return user_id and user_id == request.user.id
        