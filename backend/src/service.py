from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError()
