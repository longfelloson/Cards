import uuid
from datetime import datetime

from database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    collection_decks = relationship(
        "CollectionDeck", back_populates="collection", cascade="all, delete-orphan"
    )
    decks = relationship(
        "Deck",
        secondary="collections_decks",
        viewonly=True,
        lazy="selectin",
        overlaps="collection_decks",
    )


class CollectionDeck(Base):
    __tablename__ = "collections_decks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("collections.id", ondelete="CASCADE"),
        nullable=False,
    )
    deck_id = Column(
        UUID(as_uuid=True), ForeignKey("decks.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, default=datetime.now)

    collection = relationship(
        "Collection", back_populates="collection_decks", overlaps="decks"
    )

    deck = relationship("Deck", back_populates="collection_decks", overlaps="decks")
