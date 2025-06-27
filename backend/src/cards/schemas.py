from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict

from cards.enums import MemorizationLevel
from schemas import BaseUpdate
from schemas import BaseFilter


class CardCreate(BaseModel):
    face: str
    turnover: str
    deck_id: UUID4


class CardView(BaseModel):
    id: UUID4
    face: str
    turnover: str
    created_at: datetime
    user_id: UUID4
    deck_id: UUID4
    last_memorization_level: Optional[MemorizationLevel]
    next_review_at: Optional[datetime]
    reviews_amount: int
    ease_factor: float
    repetition_interval: int
    last_reviewed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class CardUpdate(BaseUpdate):
    _object_name = "card"

    face: Optional[str] = None
    turnover: Optional[str] = None
    last_memorization_level: Optional[MemorizationLevel] = None


class CardFilter(BaseFilter):
    face: Optional[str] = None
    turnover: Optional[str] = None
    user_id: Optional[UUID4] = None


class CardsFilter(BaseFilter):
    deck_id: Optional[UUID4] = None
    to_study: Optional[bool] = None
    user_id: Optional[UUID4] = None


class CardReview(BaseModel):
    next_review_at: datetime
    reviews_amount: int
    ease_factor: float
    repetition_interval: int
    last_reviewed_at: datetime
