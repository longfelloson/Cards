from datetime import datetime, timedelta

from auth.password import verify_password
from auth.token import create_token
from auth.verification.exceptions import (
    SameEmailException,
    SamePasswordException,
    TooManyVerificationsException,
    VerificationEmailSendException,
)
from auth.verification.utils import (
    decode_verification_token,
    send_verification_link,
)
from emails.exceptions import EmailSendException
from logger import logger
from pydantic import EmailStr
from unit_of_work import UnitOfWork
from users.models import User

VERIFICATION_COOLDOWN = timedelta(minutes=15)


class VerificationService:
    async def verify(
        self,
        *,
        user: User,
        uow: UnitOfWork,
        new_email: EmailStr = None,
        new_password: str = None,
    ):
        token_data = {"user_id": user.id}
        verification_token = create_token(token_data)

        async with uow:
            last_verification = await uow.verification.get_last(user_id=user.id)
            if (
                last_verification
                and last_verification.created_at
                >= datetime.now() - VERIFICATION_COOLDOWN
            ):
                raise TooManyVerificationsException()

            await self.send_verification_email(
                user=user,
                verification_token=verification_token,
                new_email=new_email,
                new_password=new_password,
            )
            await uow.verification.create(
                token=verification_token, email=new_email, user_id=user.id
            )

    async def send_verification_email(
        self,
        *,
        user: User,
        verification_token: str,
        new_email: EmailStr = None,
        new_password: str = None,
    ) -> None:
        """Send an email to with verification link

        Raises:
            MissingEmailException: If new_email is not provided.
            EmailAlreadyInUseException: If the new_email matches the current user email.
            EmailSendingFailedException: If sending the verification email fails.
        """
        if new_password and verify_password(new_password, user.password):
            raise SamePasswordException()

        if new_email == user.email:
            raise SameEmailException()

        email = new_email if new_email else user.email

        try:
            await send_verification_link(email, verification_token)
        except EmailSendException:
            logger.error(msg="Failed to send verification email", exc_info=True)
            raise VerificationEmailSendException()

    async def confirm(self, *, token: str, uow: UnitOfWork) -> None:
        email = decode_verification_token(token=token)
        async with uow:
            await uow.verification.update(email=email)


verification_service = VerificationService()
