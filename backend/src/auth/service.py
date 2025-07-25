from auth.exceptions import InvalidCredentialsError
from auth.password import verify_password
from auth.schemas import AccessToken
from auth.token import create_token
from unit_of_work import UnitOfWork
from users.schemas import UserCredentials, UserFilter
from users.service import users_service


class AuthService:
    def __init__(self, *, users_service):
        self.users_service = users_service

    async def login(
        self, *, credentials: UserCredentials, uow: UnitOfWork
    ) -> AccessToken:
        """Check if a user's credentials are correct and create an access token"""
        user_filter = UserFilter(email=credentials.email)
        user = await users_service.get_by(filter=user_filter, uow=uow)
        if not user:
            raise InvalidCredentialsError()

        if not verify_password(credentials.password, user.password):
            raise InvalidCredentialsError()

        access_token = create_token(data={"sub": user.email})
        return AccessToken(access_token=access_token)


auth_service = AuthService(users_service=users_service)
