from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

from decks.schemas import DeckView
from schemas import BaseUpdate, BaseFilter


class CollectionCreate(BaseModel):
    name: str
    decks_ids: list[UUID4]


class CollectionView(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    decks: list[DeckView]


class CollectionUpdate(BaseUpdate):
    _object_name = "collection"

    name: Optional[str] = None
    decks_ids: Optional[list[UUID4]] = None


class CollectionFilter(BaseFilter):
    name: str = None


class CollectionsFilter(BaseFilter):
    user_id: Optional[UUID4] = None
