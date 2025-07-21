import uuid

from enums import Visibility
from database import Base
from sqlalchemy import UUID, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Card(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    face = Column(String(64), nullable=False)
    turnover = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    deck_id = Column(
        UUID(as_uuid=True),
        ForeignKey("decks.id"),
        nullable=False,
        index=True,
    )
    last_memorization_level = Column(String(16), nullable=True)
    next_review_at = Column(DateTime, nullable=True)
    reviews_amount = Column(Integer, nullable=False, default=0)
    ease_factor = Column(Float, nullable=False, default=2.5)
    repetition_interval = Column(Integer, nullable=False, default=1)
    last_reviewed_at = Column(DateTime, nullable=True)
    visibility = Column(String(16), nullable=False, default=Visibility.hidden)
    
    user = relationship("User", back_populates="cards")
    deck = relationship("Deck", back_populates="cards")
