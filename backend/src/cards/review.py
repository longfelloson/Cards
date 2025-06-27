from datetime import datetime, timedelta

from cards.enums import MemorizationLevel, MemorizationLevelQuality
from cards.models import Card
from cards.schemas import CardReview


def get_card_review(
    last_memorization_level: MemorizationLevel, card: Card
) -> CardReview:
    """
    Calculate spaced repetition parameters based on the last memorization level.
    Returns a CardReview with updated review data.
    """
    last_reviewed_at = datetime.now()
    quality = last_memorization_level.quality

    if quality == MemorizationLevelQuality.AGAIN:
        next_review_at = datetime.now() + timedelta(minutes=1)
        card_review = CardReview(
            next_review_at=next_review_at,
            reviews_amount=card.reviews_amount,  # Do not increment
            ease_factor=card.ease_factor,
            repetition_interval=1,
            last_reviewed_at=last_reviewed_at,
        )
        return card_review

    updated_reviews_amount = card.reviews_amount + 1
    updated_ease_factor = get_updated_ease_factor(quality, card.ease_factor)
    updated_repetition_interval = get_updated_repetition_interval(
        card, updated_ease_factor, updated_reviews_amount
    )

    next_review_at = last_reviewed_at + timedelta(days=updated_repetition_interval)

    card_review = CardReview(
        next_review_at=next_review_at,
        reviews_amount=updated_reviews_amount,
        ease_factor=updated_ease_factor,
        repetition_interval=updated_repetition_interval,
        last_reviewed_at=last_reviewed_at,
    )
    return card_review


def get_updated_ease_factor(quality: int, ease_factor: float) -> float:
    ease_factor += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    return max(ease_factor, 1.3)


def get_updated_repetition_interval(
    card: Card, ease_factor: float, reviews_amount: int
) -> int:
    if reviews_amount == 1:
        return 1
    elif reviews_amount == 2:
        return 6
    else:
        return int(card.repetition_interval * ease_factor)
