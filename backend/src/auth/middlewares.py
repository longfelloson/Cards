from fastapi import Request
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
)

from auth.exceptions import TokenError
from auth.token import decode_token
from logger import logger
from unit_of_work import UnitOfWork
from config import settings
from users.schemas import UserFilter


class AuthMiddleware(AuthenticationBackend):
    async def authenticate(self, request: Request) -> AuthCredentials | None:
        if request.url.path in settings.unprotected_paths:
            return None

        token = request.cookies.get("token")
        uow = UnitOfWork()

        try:
            token_payload = decode_token(token)
            user_filter = UserFilter(email=token_payload["sub"])

            async with uow:
                user = await uow.users.get_by(filter=user_filter)
        except TokenError as exc:
            logger.warning("Failed to authenticate a user: ", exc_info=True)
            raise exc

        request.state.uow = uow

        return AuthCredentials(["authenticated"]), user
