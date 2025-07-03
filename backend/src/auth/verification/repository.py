from typing import Optional
from pydantic import EmailStr, UUID4
from sqlalchemy import insert, select, update
from auth.verification.models import Verification
from repository import SQLAlchemyRepository


class VerificationRepository(SQLAlchemyRepository):
    model = Verification

    async def create(self, *, token: str, email: EmailStr, user_id: UUID4) -> None:
        await self.session.execute(
            insert(self.model).values(email=email, token=token, user_id=user_id)
        )
        await self.session.commit()

    async def get(self, *, email: EmailStr) -> Optional[Verification]:
        verification = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return verification.scalar_one_or_none()

    async def update(self, *, email: EmailStr) -> None:
        await self.session.execute(
            update(self.model)
            .values({self.model.is_verified: True})
            .where(self.model.email == email)
        )
        await self.session.commit()
