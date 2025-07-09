from typing import Annotated

from auth.exceptions import InvalidTokenException
from auth.token import decode_token, oauth2_scheme
from dependencies import UOWDependency
from fastapi import Depends
from users.models import User
from users.schemas import UserFilter
from users.service import users_service


async def get_current_user(
    uow: UOWDependency,
    token: str = Depends(oauth2_scheme),
) -> User:
    """Get a current user from JWT by a request"""
    token_payload = decode_token(token)
    user_filter = UserFilter(email=token_payload["sub"])
    user = await users_service.get_by(filter=user_filter, uow=uow)
    if not user:
        raise InvalidTokenException()
    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
