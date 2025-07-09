from exceptions import AlreadyExistsException, NotFoundException

USER_OBJECT_NAME = "user"


class UserNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(object_name=USER_OBJECT_NAME)


class UserAlreadyExistsException(AlreadyExistsException):
    def __init__(self):
        super().__init__(object_name=USER_OBJECT_NAME)
