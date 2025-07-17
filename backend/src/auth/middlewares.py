from typing import Any

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from auth.exceptions import TokenError
from auth.utils import get_user_from_token
from users.models import User
from unit_of_work import UnitOfWork
from config import settings
from logger import logger


class _AuthenticationError(AuthenticationError):
    def __init__(
        self,
        *,
        code: int | None = None,
        msg: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.msg = msg
        self.headers = headers


class AuthMiddleware(AuthenticationBackend):
    @staticmethod
    def auth_exception_handler(
        _: HTTPConnection, exc: _AuthenticationError
    ) -> Response:
        return JSONResponse(
            content={"code": exc.code, "msg": exc.msg},
            status_code=exc.code,
        )

    async def authenticate(self, request: Request) -> AuthCredentials | None:
        if request.url.path in settings.unprotected_paths:
            return None

        token = request.cookies.get("token")
        uow = UnitOfWork()

        try:
            user: User = await get_user_from_token(token, uow)
        except TokenError as exc:
            raise _AuthenticationError(
                code=exc.status_code, msg=exc.detail, headers=exc.headers
            )
        except Exception as exc:
            logger.error("Unexpected error in AuthMiddleware", exc_info=True)
            raise _AuthenticationError(
                code=getattr(exc, "status_code", 500),
                msg=getattr(exc, "detail", "Internal Server Error"),
            )

        request.state.uow = uow

        return AuthCredentials(["authenticated"]), user
