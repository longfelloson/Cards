from enum import StrEnum


class Role(StrEnum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"


class Resource(StrEnum):
    USERS = "users"
    CARDS = "cards"
    DECKS = "decks"
    COLLECTIONS = "collections"


class Action(StrEnum):
    CREATE = "post"
    READ = "get"
    UPDATE = "patch"
    DELETE = "delete"
