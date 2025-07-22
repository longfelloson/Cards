import uuid
from datetime import datetime

from enums import Visibility
from database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String


class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    visibility = Column(String(16), nullable=False, default=Visibility.hidden)


class CollectionDeck(Base):
    __tablename__ = "collection_decks"

    deck_id = Column(
        UUID(as_uuid=True),
        ForeignKey("decks.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    collection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("collections.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now)
