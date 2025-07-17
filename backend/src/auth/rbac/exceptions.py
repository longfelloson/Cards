from exceptions import NotFoundException


class ResourceNotFound(NotFoundException):
    def __init__(self):
        super().__init__(object_name="resource")
