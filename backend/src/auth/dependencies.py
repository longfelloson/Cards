from typing import Annotated

from auth.exceptions import InvalidTokenError
from auth.utils import get_user_from_token
from auth.permissions import BasePermission
from fastapi import Depends, Request
from users.models import User
from users.schemas import UserFilter
from users.service import users_service


async def get_current_user(
    request: Request,
) -> User:
    """Get a current user from JWT by a request"""
    token = request.cookies.get("token")
    user = await get_user_from_token(token, request.state.uow)
    if not user:
        raise InvalidTokenError()
    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
