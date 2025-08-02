from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from enums import Visibility
from deck_collections.models import Collection
from schemas import BaseFilter, BaseUpdate


class CollectionCreate(BaseModel):
    name: str
    deck_ids: list[UUID4]


class CollectionView(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    user_id: UUID4
    visibility: Visibility


class CollectionUpdate(BaseUpdate):
    object_name = "collection"
    model = Collection

    name: Optional[str] = None
    decks_ids: Optional[list[UUID4]] = None
    visibility: Optional[Visibility] = None


class CollectionFilter(BaseFilter):
    name: str = None


class CollectionsFilter(BaseFilter):
    user_id: Optional[UUID4] = None
    visibility: Visibility = Visibility.visible
