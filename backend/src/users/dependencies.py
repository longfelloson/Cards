from typing import Annotated

from fastapi import Depends
from auth.verification.dependencies import VerificationServiceDependency
from dependencies import UOWDependency
from cache.dependencies import StorageDependency
from users.service import UsersService


def get_users_service(
    storage: StorageDependency,
    verification_service: VerificationServiceDependency,
    uow: UOWDependency,
) -> UsersService:
    service = UsersService(
        verification_service=verification_service, storage=storage, uow=uow
    )
    return service


UsersServiceDependency = Annotated[UsersService, Depends(get_users_service)]
