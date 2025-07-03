from datetime import datetime
import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from database import Base


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
    is_verified = Column(Boolean, default=False)

    cards = relationship("Card", back_populates="user")
    decks = relationship("Deck", back_populates="user")
