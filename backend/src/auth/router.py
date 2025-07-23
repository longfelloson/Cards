from fastapi import APIRouter, status

from auth.schemas import AccessToken
from auth.dependencies import AuthServiceDependency
from users.schemas import UserCredentials

router = APIRouter()


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
)
async def create_token(data: UserCredentials, service: AuthServiceDependency):
    access_token: AccessToken = await service.login(credentials=data)
    return access_token
