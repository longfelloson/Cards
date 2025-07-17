from email.message import EmailMessage
from typing import Optional
from urllib.parse import urlencode

from jwt import InvalidTokenError
from pydantic import EmailStr, HttpUrl

from auth.token import decode_token
from auth.verification.exceptions import (
    ExpiredLinkException,
    InvalidLinkException,
    MissingVerificationTokenException,
)
from auth.exceptions import ExpiredTokenError
from config import settings
from emails.utils import send_email


def decode_verification_token(*, token: Optional[str]) -> EmailStr:
    """Change a user's email to a new one"""
    if not token:
        raise MissingVerificationTokenException()

    try:
        new_email = decode_token(token)["email"]
    except ExpiredTokenError:
        raise ExpiredLinkException()
    except InvalidTokenError:
        raise InvalidLinkException()

    return new_email


async def send_verification_link(email: EmailStr, token: str) -> None:
    message = EmailMessage()

    message["From"] = settings.smtp.EMAIL
    message["To"] = email
    message["Subject"] = "Hello World!"

    verification_link = generate_verification_link(token, email)
    message.set_content(f"Your new link: {verification_link}")

    await send_email(message)


def generate_verification_link(token: str, new_email: EmailStr = None) -> HttpUrl:
    params = {"token": token}
    if new_email:
        params["email":new_email]

    verification_link = settings.verification_url + "?" + urlencode(params)
    return verification_link
