from email.message import EmailMessage
from typing import Optional
from urllib.parse import urlencode
from pydantic import UUID4, EmailStr, HttpUrl

from auth.token import create_token, decode_token
from auth.exceptions import ExpiredTokenException, InvalidTokenException
from auth.verification.exceptions import (
    ExpiredLinkException,
    InvalidLinkException,
    MissingVerificationTokenException,
)
from emails.utils import send_email
from config import settings


def decode_verification_token(*, token: Optional[str]) -> EmailStr:
    """Change a user's email to a new one"""
    if not token:
        raise MissingVerificationTokenException()

    try:
        new_email = decode_token(token)["email"]
    except ExpiredTokenException:
        raise ExpiredLinkException()
    except InvalidTokenException:
        raise InvalidLinkException()

    return new_email


async def send_verification_link(
    user_id: UUID4, new_email: EmailStr, token: str
) -> None:
    message = EmailMessage()

    message["From"] = settings.smtp.SMTP_EMAIL
    message["To"] = new_email
    message["Subject"] = "Hello World!"

    verification_link = generate_verification_link(user_id, token, new_email)
    message.set_content(f"Your new link: {verification_link}")

    await send_email(message)


def generate_verification_token(email: EmailStr) -> str:
    data = {"email": email}
    verification_token = create_token(data=data)
    return verification_token


def generate_verification_link(
    user_id: UUID4, token: str, new_email: EmailStr
) -> HttpUrl:
    params = {"user_id": user_id, "token": token, "email": new_email}
    verification_link = settings.verification_url + "?" + urlencode(params)
    return verification_link
