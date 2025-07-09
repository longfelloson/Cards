import uuid
from datetime import datetime

from database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Deck(Base):
    __tablename__ = "decks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    collection_decks = relationship(
        "CollectionDeck", back_populates="deck", overlaps="decks"
    )
    user = relationship("User", back_populates="decks")
    cards = relationship("Card", back_populates="deck", cascade="all, delete-orphan")
