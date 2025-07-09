import uuid
from datetime import datetime

from auth.rbac.enums import Role
from database import Base
from sqlalchemy import UUID, Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email = Column(
        String,
        nullable=False,
        unique=True,
    )
    password = Column(
        String(128),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )
    role = Column(String(32), nullable=False, default=Role.USER)
    is_verified = Column(Boolean, nullable=False, default=False)

    cards = relationship("Card", back_populates="user")
    decks = relationship("Deck", back_populates="user")
