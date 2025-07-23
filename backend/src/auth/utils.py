from typing import Optional

from auth.token import decode_token
from users.service import UsersService
from users.models import User
from users.schemas import UserFilter


async def get_user_from_token(token: str, users_service: UsersService) -> Optional[User]:
    token_payload = decode_token(token)
    user_filter = UserFilter(email=token_payload["sub"])
    user = await users_service.get_by(filter=user_filter)
    return user
