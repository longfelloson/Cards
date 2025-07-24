from enum import StrEnum

from cache.namespaces import Namespace


class Key(StrEnum):
    DECK = Namespace.DECK + ":{deck_id}"
    DECKS = Namespace.DECKS + ":{filter}"
    
    CARD = Namespace.CARD + ":{card_id}"
    CARDS = Namespace.CARDS + ":{filter}"
    
    USER = Namespace.USER + ":{user_id}"
    USERS = Namespace.USERS + ":{filter}"
    
    COLLECTION = Namespace.COLLECTION + ":{collection_id}"
    COLLECTIONS = Namespace.COLLECTIONS + ":{filter}"
    