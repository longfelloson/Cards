from abc import ABC, abstractmethod
from typing import Optional

from pydantic import UUID4, BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create(self, data: BaseModel, user_id: Optional[UUID4] = None):
        create_data = data.model_dump()
        if user_id:
            create_data["user_id"] = user_id

        obj = self.model(**create_data)
        self.session.add(obj)

        await self.session.flush()
        await self.session.commit()

        return obj

    async def get(self, *, id: UUID4):
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by(self, *, filter):
        conditions = filter.get_conditions(self.model)
        res = await self.session.execute(select(self.model).where(*conditions))
        return res.scalar_one_or_none()

    async def get_all(self, *, filter) -> list:
        conditions = filter.get_conditions(self.model)
        stmt = select(self.model).where(*conditions)
        res = await self.session.execute(stmt.offset(filter.offset).limit(filter.limit))
        return res.scalars().all()

    async def update(self, *, obj, data):
        for key, value in data.items():
            if hasattr(self.model, key):
                setattr(obj, key, value)

        self.session.add(obj)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def delete_by_obj(self, *, obj):
        await self.session.delete(obj)
        await self.session.commit()

    async def delete(self, obj_id: int | UUID4) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == obj_id))
        await self.session.commit()
