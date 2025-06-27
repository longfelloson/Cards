from fastapi import HTTPException, status

MISSING_UPDATE_DATA_TEMPLATE = "Missing required data to update the {}"
ALREADY_EXISTS_TEMPLATE = "The {} already exists"
NOT_FOUND_TEMPLATE = "The {} was not found"


class AlreadyExists(HTTPException):
    def __init__(self, object_name: str):
        super().__init__(
            detail=ALREADY_EXISTS_TEMPLATE.format(object_name),
            status_code=status.HTTP_409_CONFLICT,
        )


class NotFound(HTTPException):
    def __init__(self, object_name: str):
        super().__init__(
            detail=NOT_FOUND_TEMPLATE.format(object_name),
            status_code=status.HTTP_404_NOT_FOUND,
        )


class MissingUpdateData(HTTPException):
    def __init__(self, object_name: str):
        super().__init__(
            detail=MISSING_UPDATE_DATA_TEMPLATE.format(object_name),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
