from typing import Optional

from auth.token import decode_token
from unit_of_work import UnitOfWork
from users.models import User
from users.service import users_service
from users.schemas import UserFilter


async def get_user_from_token(token: str, uow: UnitOfWork) -> Optional[User]:
    token_payload = decode_token(token)
    user_filter = UserFilter(email=token_payload["sub"])
    user = await users_service.get_by(filter=user_filter, uow=uow)
    return user
