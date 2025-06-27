from exceptions import NotFound, AlreadyExists

USER_OBJECT_NAME = "user"


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__(object_name=USER_OBJECT_NAME)


class UserAlreadyExists(AlreadyExists):
    def __init__(self):
        super().__init__(object_name=USER_OBJECT_NAME)
