from fastapi import HTTPException, status


class AccessDeniedException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Resource doesn't exist",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)
