from exceptions import AlreadyExistsException, NotFoundException

COLLECTION_OBJECT_NAME = "collection"


class CollectionNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(object_name=COLLECTION_OBJECT_NAME)


class CollectionAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(object_name=COLLECTION_OBJECT_NAME)
