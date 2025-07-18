from typing import Annotated, Sequence

from auth.exceptions import InvalidTokenError
from auth.utils import get_user_from_token
from auth.permissions import BasePermission
from fastapi import Depends, Request
from auth.rbac.enums import Role
from users.models import User


async def get_current_user(
    request: Request,
) -> User:
    """Get a current user from JWT by a request"""
    token = request.cookies.get("token")
    user = await get_user_from_token(token, request.state.uow)
    if not user:
        raise InvalidTokenError()
    return user


class PermissionsDependency:
    def __init__(self, *permission_classes: Sequence[type[BasePermission]]):
        self.permission_classes = permission_classes

    async def __call__(self, request: Request):
        if request.user.role == Role.ADMIN:
            return
        
        for permission_class in self.permission_classes:
            permission_instance = permission_class()
            await permission_instance(request)


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
