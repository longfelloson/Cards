from enum import Enum, StrEnum


class MemorizationLevel(StrEnum):
    AGAIN = "again"
    HARD = "hard"
    GOOD = "good"
    EASY = "easy"

    @property
    def quality(self) -> int:
        qualities = {
            MemorizationLevel.AGAIN: MemorizationLevelQuality.AGAIN,
            MemorizationLevel.HARD: MemorizationLevelQuality.HARD,
            MemorizationLevel.GOOD: MemorizationLevelQuality.GOOD,
            MemorizationLevel.EASY: MemorizationLevelQuality.EASY,
        }
        return qualities[self].value


class MemorizationLevelQuality(Enum):
    AGAIN = 1
    HARD = 3
    GOOD = 4
    EASY = 5
