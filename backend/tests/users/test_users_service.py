from ssl import cert_time_to_seconds
from venv import create
from auth.password import verify_password
from unit_of_work import UnitOfWork
from users.models import User
from users.schemas import UserCreate, UserUpdate
from users.service import users_service


# TODO: tests for cards service
class TestUsersService:
    async def test_create(self, uow: UnitOfWork):
        data = UserCreate(email="", password="")
        user = await users_service.create(data=data, uow=uow)

        assert isinstance(user, User)
        assert user.email == data.email, verify_password(data.password, user.password)

    async def test_get(self, create_user: User, uow: UnitOfWork):
        user = await users_service.get(user_id=create_user.id, uow=uow)

        assert isinstance(user, User)
        assert user.id == create_user.id

    async def test_update(self, create_user: User, data: UserUpdate, uow: UnitOfWork):
        updated_user = await users_service.update(user_id=create_user, data=data)

        for attr in data.model_dump().keys():
            if hasattr(updated_user, attr):
                value = getattr(create_user)
                assert value == data[attr]

    async def test_delete(self):
        # TODO: tests for test delete
        ...
