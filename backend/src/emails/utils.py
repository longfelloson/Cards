from email.message import EmailMessage

import aiosmtplib

from emails.exceptions import EmailSendException
from config import settings
from logger import logger


async def send_email(message: EmailMessage) -> None:
    try:
        await aiosmtplib.send(message, **settings.smtp.send_email_kwargs)
    except aiosmtplib.SMTPException as e:
        logger.error(msg="Error while sending a message via email", exc_info=True)
        raise EmailSendException() from e
        