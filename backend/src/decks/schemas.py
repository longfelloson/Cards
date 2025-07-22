from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from enums import Visibility
from decks.models import Deck
from schemas import BaseFilter, BaseUpdate


class DeckCreate(BaseModel):
    name: str


class DeckView(BaseModel):
    id: UUID4
    name: str
    user_id: UUID4
    created_at: datetime
    visibility: Visibility


class DeckUpdate(BaseUpdate):
    object_name = "deck"
    model = Deck

    name: Optional[str] = None
    visibility: Optional[Visibility] = None


class DecksFilter(BaseFilter):
    user_id: Optional[UUID4] = None
    collection_id: Optional[UUID4] = None
    to_study: Optional[bool] = None
    visibility: Visibility = Visibility.visible


class DeckFilter(BaseFilter):
    name: Optional[str] = None
    user_id: Optional[UUID4] = None
