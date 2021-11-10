from typing import Optional, Dict

from grinx.responses.errors import ErrorBaseResponse


class BaseGrinxException(BaseException):
    def __init__(self, exception_code: int,
                 user_readable_message: str,
                 content: Optional[bytes] = None,
                 headers: Optional[Dict[str, str]] = None):
        self.exception_code = exception_code
        self.user_readable_message = user_readable_message
        self.content = content
        self.headers = headers

    def to_response(self):
        return ErrorBaseResponse(self.exception_code,
                                 self.user_readable_message,
                                 content=self.content,
                                 headers=self.headers)
