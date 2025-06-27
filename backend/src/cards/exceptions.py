from exceptions import AlreadyExists, NotFound

CARD_OBJECT_NAME = "card"


class CardNotFound(NotFound):
    def __init__(self):
        super().__init__(object_name=CARD_OBJECT_NAME)


class CardAlreadyExists(AlreadyExists):
    def __init__(self):
        super().__init__(object_name=CARD_OBJECT_NAME)
