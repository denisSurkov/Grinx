from typing import Optional

from grinx.exceptions.base import BaseGrinxException


class BadGrinxRequest(BaseGrinxException):
    def __init__(self, what_went_wrong: Optional[str] = None):
        super().__init__(400, 'Bad Request')
        if what_went_wrong:
            self.content = bytes(what_went_wrong, 'utf8')
