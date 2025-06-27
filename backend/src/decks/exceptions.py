from exceptions import NotFound, AlreadyExists

DECK_OBJECT_NAME = "deck"


class DeckNotFound(NotFound):
    def __init__(self):
        super().__init__(object_name=DECK_OBJECT_NAME)


class DeckAlreadyExists(AlreadyExists):
    def __init__(self):
        super().__init__(object_name=DECK_OBJECT_NAME)
