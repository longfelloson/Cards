from typing import Annotated

from auth.exceptions import InvalidTokenError
from auth.utils import get_user_from_token
from fastapi import Depends, Request
from auth.service import AuthService
from users.dependencies import UsersServiceDependency
from users.models import User


async def get_current_user(
    request: Request,
    users_service: UsersServiceDependency
) -> User:
    """Get a current user from JWT by a request"""
    token = request.cookies.get("token")
    user = await get_user_from_token(token, users_service)
    if not user:
        raise InvalidTokenError()
    return user


def get_auth_service(users_service: UsersServiceDependency) -> AuthService:
    service = AuthService(users_service=users_service)
    return service


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]
