from typing import Optional

from responses.errors import ErrorBaseResponse


class BaseGrinxException(BaseException):
    def __init__(self, exception_code: int, user_readable_message: str, content: Optional[bytes] = None):
        self.exception_code = exception_code
        self.user_readable_message = user_readable_message
        self.content = content

    def to_response(self):
        return ErrorBaseResponse(self.exception_code, self.user_readable_message, content=self.content)
