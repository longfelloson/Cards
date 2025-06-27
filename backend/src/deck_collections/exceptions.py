from exceptions import NotFound, AlreadyExists

COLLECTION_OBJECT_NAME = "collection"


class CollectionNotFound(NotFound):
    def __init__(self):
        super().__init__(object_name=COLLECTION_OBJECT_NAME)


class CollectionAlreadyExists(AlreadyExists):
    def __init__(self):
        super().__init__(object_name=COLLECTION_OBJECT_NAME)
