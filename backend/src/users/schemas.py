from datetime import datetime
from typing import Optional
from pydantic import UUID4, EmailStr, BaseModel, Field

from users.models import User
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
    object_name = "user"
    model = User

    password: Optional[str] = None
    email: Optional[EmailStr] = None

    verify_email: Optional[bool] = Field(
        default=None,
        description="Provide True if you need to send verification email to provided email",
    )
    verification_token: Optional[str] = Field(
        default=None,
        description="Token has to be provided to check if email was verified",
    )


class UserFilter(BaseFilter):
    email: Optional[EmailStr] = None


class UsersFilter(BaseFilter): ...
