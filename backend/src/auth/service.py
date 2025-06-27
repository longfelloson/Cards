from auth.schemas import AccessToken
from auth.exceptions import InvalidCredentialsException
from auth.password import verify_password
from auth.token import create_access_token
from unit_of_work import UnitOfWork
from users.schemas import UserCredentials, UserFilter
from users.service import users_service


class AuthService:
    async def login(
        self, *, credentials: UserCredentials, uow: UnitOfWork
    ) -> AccessToken:
        user_filter = UserFilter(email=credentials.email)
        user = await users_service.get_by(filter=user_filter, uow=uow)
        if not user:
            raise InvalidCredentialsException()

        if not verify_password(credentials.password, user.password):
            raise InvalidCredentialsException()

        access_token = create_access_token(data={"sub": user.email})
        return access_token


auth_service = AuthService()
