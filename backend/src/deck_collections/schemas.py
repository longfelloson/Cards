from datetime import datetime
from typing import Optional

from deck_collections.models import Collection
from decks.schemas import DeckView
from pydantic import UUID4, BaseModel
from schemas import BaseFilter, BaseUpdate


class CollectionCreate(BaseModel):
    name: str
    decks_ids: list[UUID4]


class CollectionView(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    decks: list[DeckView]


class CollectionUpdate(BaseUpdate):
    object_name = "collection"
    model = Collection

    name: Optional[str] = None
    decks_ids: Optional[list[UUID4]] = None


class CollectionFilter(BaseFilter):
    name: str = None


class CollectionsFilter(BaseFilter):
    user_id: Optional[UUID4] = None
