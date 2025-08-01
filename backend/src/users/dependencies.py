from typing import Annotated

from fastapi import Depends
from auth.dependencies import CurrentUserDependency
from auth.verification.dependencies import VerificationServiceDependency
from dependencies import UOWDependency
from cache.dependencies import StorageDependency
from users.service import UsersService


async def get_users_service(
    storage: StorageDependency,
    verification_service: VerificationServiceDependency,
    uow: UOWDependency,
    user: CurrentUserDependency,
) -> UsersService:
    service = UsersService(
        verification_service=verification_service,
        storage=storage,
        uow=uow,
        user=user,
    )
    return service


UsersServiceDependency = Annotated[UsersService, Depends(get_users_service)]
