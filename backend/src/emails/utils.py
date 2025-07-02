from email.message import EmailMessage
import aiosmtplib

from config import settings


async def send_email(message: EmailMessage) -> None:
    await aiosmtplib.send(
        message,
        hostname=settings.smtp.SMTP_HOST,
        port=settings.smtp.SMTP_PORT,
        start_tls=True,
        username=settings.smtp.SMTP_EMAIL,
        password=settings.smtp.SMTP_PASSWORD.get_secret_value(),
    )
