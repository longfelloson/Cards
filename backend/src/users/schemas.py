from datetime import datetime
from typing import Optional
from pydantic import UUID4, EmailStr, BaseModel

from schemas import BaseUpdate, BaseFilter


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserCredentials): ...


class UserView(BaseModel):
    id: UUID4
    email: EmailStr
    created_at: datetime


class UserUpdate(BaseUpdate):
    __object_name = "user"

    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserFilter(BaseFilter):
    email: Optional[EmailStr] = None


class UsersFilter(BaseFilter): ...
