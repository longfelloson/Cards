from users.models import User
from repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
