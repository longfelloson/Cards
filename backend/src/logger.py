from enum import StrEnum
import logging

from config import settings


class LoggingLevel(StrEnum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"
    CRITICAL = "CRITICAL"
    
    
logger = logging.Logger(__name__)
logger.setLevel(lever=settings.logging.LOGGING_LEVEL)

handler = logging.FileHandler(filename=settings.logging.LOGGING_FILENAME)
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)
