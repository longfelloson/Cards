from typing import Dict, Optional
from fastapi import HTTPException, status


class InvalidLinkException(HTTPException):
    """Raised when the provided verification token is invalid"""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "The verification token of the link is invalid",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class ExpiredLinkException(HTTPException):
    """Raises when user clicked an expired link"""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "The entered code is expired",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class EmailMismatchException(HTTPException):
    """Raises when user entered an email that is already in use"""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "The email of the link is incorrect",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class SameEmailException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You cannot reuse your current email",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class SamePasswordException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You cannot reuse your current password",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class MissingEmailException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No email was provided to send a verification link",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class MissingVerificationTokenException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "No token was provided to verify email",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class TooManyVerificationsException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Too many verification requests",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)


class VerificationEmailSendException(HTTPException):
    def __init__(
        self,
        detail: str = "Failed to send verification email",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
