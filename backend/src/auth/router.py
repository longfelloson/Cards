from fastapi import APIRouter, status

from auth.schemas import AccessToken
from auth.service import auth_service
from dependencies import UOWDependency
from users.schemas import UserCredentials

router = APIRouter()


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
)
async def create_token(
    uow: UOWDependency,
    data: UserCredentials,
):
    access_token: AccessToken = await auth_service.login(credentials=data, uow=uow)
    return access_token
