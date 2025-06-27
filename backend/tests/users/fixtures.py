import pytest_asyncio

from unit_of_work import UnitOfWork
from users.models import User
from users.service import users_service


@pytest_asyncio.fixture
async def create_user(data, uow: UnitOfWork) -> User:
    # TODO: check this fixture
    user = await users_service.create(data=data, uow=uow)
    return user
