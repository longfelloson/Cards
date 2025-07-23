from typing import Annotated, Any

from fastapi import Depends
from auth.verification.service import VerificationService


def get_verification_service() -> VerificationService:
    service = VerificationService()
    return service


VerificationServiceDependency = Annotated[VerificationService, Depends(get_verification_service)]
