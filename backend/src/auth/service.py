from auth.schemas import AccessToken
from auth.password import verify_password
from auth.token import create_token
from auth.exceptions import InvalidCredentialsException
from unit_of_work import UnitOfWork
from users.schemas import UserCredentials, UserFilter
from users.service import users_service


class AuthService:
    async def login(
        self, *, credentials: UserCredentials, uow: UnitOfWork
    ) -> AccessToken:
        """Check if a user's credentials are correct and create an access token"""
        user_filter = UserFilter(email=credentials.email)
        user = await users_service.get_by(filter=user_filter, uow=uow)
        if not user:
            raise InvalidCredentialsException()

        if not verify_password(credentials.password, user.password):
            raise InvalidCredentialsException()

        access_token = create_token(data={"sub": user.email})
        return AccessToken(access_token=access_token)


auth_service = AuthService()
