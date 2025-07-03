from abc import ABC, abstractmethod

from auth.verification.repository import VerificationRepository
from deck_collections.repository import CollectionDecksRepository, CollectionsRepository
from decks.repository import DecksRepository
from users.repository import UsersRepository
from database import async_session_maker
from cards.repository import CardsRepository


class IUnitOfWork(ABC):
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.cards = CardsRepository(self.session)
        self.decks = DecksRepository(self.session)
        self.collections = CollectionsRepository(self.session)
        self.collection_decks = CollectionDecksRepository(self.session)
        self.verification = VerificationRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
