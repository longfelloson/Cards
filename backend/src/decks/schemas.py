from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel
from schemas import BaseFilter, BaseUpdate


class DeckCreate(BaseModel):
    name: str


class DeckView(BaseModel):
    id: UUID4
    name: str
    user_id: UUID4
    created_at: datetime


class DeckUpdate(BaseUpdate):
    _object_name = "deck"

    name: Optional[str] = None


class DecksFilter(BaseFilter):
    user_id: Optional[UUID4] = None
    collection_id: Optional[UUID4] = None
    to_study: Optional[bool] = None


class DeckFilter(BaseFilter):
    name: Optional[str] = None
    user_id: Optional[UUID4] = None


class CollectionDeckView(BaseModel):
    id: UUID4
    collection_id: UUID4
    created_at: datetime
