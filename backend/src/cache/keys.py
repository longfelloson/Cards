from enum import StrEnum

from pydantic import UUID4

from cache.namespaces import Namespace
from config import settings


class Key(StrEnum):
    @classmethod
    def deck(cls, deck_id: UUID4) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.DECK}:{deck_id}"

    @classmethod
    def decks(cls) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.DECKS}"

    @classmethod
    def user(cls, user_id: UUID4) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.USER}:{user_id}"

    @classmethod
    def users(cls) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.USERS}"

    @classmethod
    def collection(cls, collection_id: UUID4) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.COLLECTION}:{collection_id}"

    @classmethod
    def collections(cls) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.COLLECTIONS}"

    @classmethod
    def card(cls, card_id: UUID4) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.CARD}:{card_id}"

    @classmethod
    def cards(cls) -> str:
        return f"{settings.redis.DB_PREFIX}:{Namespace.CARDS}"
