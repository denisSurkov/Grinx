from typing import Optional

from grinx.responses.base import BaseResponse


class ErrorBaseResponse(BaseResponse):
    ...


class NotFoundResponse(ErrorBaseResponse):
    def __init__(self, content: Optional[bytes] = None, headers: Optional[bytes] = None):
        super().__init__(404, 'Not Found', content, headers)
