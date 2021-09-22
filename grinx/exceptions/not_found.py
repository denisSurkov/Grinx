from exceptions.base import BaseGrinxException


class GrinxFileNotFoundException(BaseGrinxException):
    def __init__(self, what_file: str):
        super().__init__(
            exception_code=404,
            user_readable_message='Not Found',
            content=bytes(what_file, 'utf8'),
        )

