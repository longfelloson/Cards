from exceptions import AlreadyExistsException, NotFoundException

CARD_OBJECT_NAME = "card"


class CardNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(object_name=CARD_OBJECT_NAME)


class CardAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(object_name=CARD_OBJECT_NAME)
