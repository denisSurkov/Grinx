from typing import Optional

from exceptions.base import BaseGrinxException


class BadGrinxRequest(BaseGrinxException):
    def __init__(self, what_went_wrong: Optional[str] = None):
        self.exception_code = 400
        self.message = 'Bad Request'
        if what_went_wrong:
            self.content = bytes(what_went_wrong, 'utf8')
