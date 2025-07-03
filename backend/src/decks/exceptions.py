from exceptions import NotFoundException, AlreadyExistsException

DECK_OBJECT_NAME = "deck"


class DeckNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(object_name=DECK_OBJECT_NAME)


class DeckAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(object_name=DECK_OBJECT_NAME)
