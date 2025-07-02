from fastapi import HTTPException, status


class EmailSendingFailedException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Failed to send verification email",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)
