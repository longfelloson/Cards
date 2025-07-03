from typing import Optional

from pydantic import EmailStr

from auth.verification.utils import (
    decode_verification_token,
    generate_verification_token,
    send_verification_link,
)
from emails.exceptions import EmailSendingFailedException
from auth.verification.exceptions import (
    EmailAlreadyInUseException,
    MissingEmailException,
)
from unit_of_work import UnitOfWork
from users.models import User


class VerificationService:
    async def send_verification_email(
        self, *, new_email: Optional[EmailStr], user: User, uow: UnitOfWork
    ) -> None:
        """Generate and send a verification email with a token for the new email address.

        Raises:
            MissingEmailException: If new_email is not provided.
            EmailAlreadyInUseException: If the new_email matches the current user email.
            EmailSendingFailedException: If sending the verification email fails.
        """
        if not new_email:
            raise MissingEmailException()

        if new_email == user.email:
            raise EmailAlreadyInUseException()

        verification_token = generate_verification_token(email=new_email)

        try:
            await send_verification_link(user.id, new_email, verification_token)
        except Exception as e:
            raise EmailSendingFailedException() from e

        async with uow:
            await uow.verification.create(
                token=verification_token, email=new_email, user_id=user.id
            )

    async def confirm_email(self, *, token: str, uow: UnitOfWork) -> None:
        email = decode_verification_token(token=token)
        async with uow:
            await uow.verification.update(email=email)


verification_service = VerificationService()
