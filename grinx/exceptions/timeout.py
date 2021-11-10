from grinx.exceptions.base import BaseGrinxException


class GrinxTimeoutException(BaseGrinxException):
    def __init__(self):
        super().__init__(
                exception_code=408,
                user_readable_message='Request Timeout',
                headers={
                    'Connection': 'close',
                },
        )
