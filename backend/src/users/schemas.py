from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field
from schemas import BaseFilter, BaseUpdate
from users.models import User


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserCredentials): ...


class UserView(BaseModel):
    id: UUID4
    email: EmailStr
    created_at: datetime


class UserUpdate(BaseUpdate):
    object_name = "user"
    model = User

    password: Optional[str] = None
    email: Optional[EmailStr] = None

    verify: Optional[bool] = Field(
        default=None,
        description="Provide True if you need to verify the password or the email",
    )
    verification_token: Optional[str] = Field(
        default=None,
        description="Token has to be provided to check if email was verified",
    )


class UserFilter(BaseFilter):
    email: Optional[EmailStr] = None


class UsersFilter(BaseFilter): ...
