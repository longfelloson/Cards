from email.message import EmailMessage

import aiosmtplib

from emails.exceptions import EmailSendException
from config import settings
from logger import logger


async def send_email(message: EmailMessage) -> None:
    try:
        await aiosmtplib.send(
            message,
            hostname=settings.smtp.SMTP_HOST,
            port=settings.smtp.SMTP_PORT,
            start_tls=True,
            username=settings.smtp.SMTP_EMAIL,
            password=settings.smtp.SMTP_PASSWORD.get_secret_value(),
        )
    except aiosmtplib.SMTPException as e:
        logger.error(msg="Error while sending a message via email", exc_info=True)
        raise EmailSendException() from e
    