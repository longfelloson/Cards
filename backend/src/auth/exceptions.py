from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Incorrect username or password",
        headers: dict = {"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(status_code, detail, headers)


class ExpiredTokenException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Token expired",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class InvalidTokenException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Invalid token",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)
