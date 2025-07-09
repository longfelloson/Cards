from typing import Optional

from auth.verification.models import Verification
from pydantic import UUID4, EmailStr
from repository import SQLAlchemyRepository
from sqlalchemy import insert, select, update


class VerificationRepository(SQLAlchemyRepository):
    model = Verification

    async def create(
        self,
        *,
        token: str,
        user_id: UUID4,
        email: EmailStr = None,
        password: str = None,
    ) -> None:
        await self.session.execute(
            insert(self.model).values(
                email=email, password=password, token=token, user_id=user_id
            )
        )
        await self.session.commit()

    async def get(self, *, email: EmailStr) -> Optional[Verification]:
        verification = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return verification.scalar_one_or_none()

    async def get_last(self, *, user_id: UUID4) -> Optional[Verification]:
        verification = await self.session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )
        return verification

    async def update(self, *, email: EmailStr) -> None:
        await self.session.execute(
            update(self.model)
            .values({self.model.is_verified: True})
            .where(self.model.email == email)
        )
        await self.session.commit()
