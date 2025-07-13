class EmailSendException(Exception):
    def __init__(self, detail: str = "Email send failed"):
        super().__init__(detail)
