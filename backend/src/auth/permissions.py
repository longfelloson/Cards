from abc import ABC, abstractmethod

from fastapi import HTTPException, Request

from auth.rbac.exceptions import ResourceNotFound


def any_permission(permissions: list, request: Request) -> bool:
    for p in permissions:
        try:
            p(request=request)
            return True
        except HTTPException:
            pass
    return False


class BasePermission(ABC):
    async def __call__(self, request: Request):
        if not await self.has_required_permissions(request):
            raise ResourceNotFound()

    @abstractmethod
    async def has_required_permissions(self, request: Request) -> bool:
        raise NotImplementedError()
