import logging

from config import settings


logger = logging.Logger(__name__)
logger.setLevel(level=settings.logging.LEVEL)

handler = logging.FileHandler(filename=settings.logging.FILENAME)
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)
