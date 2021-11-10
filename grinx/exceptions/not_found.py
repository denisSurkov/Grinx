from grinx.exceptions.base import BaseGrinxException


class GrinxNotFoundException(BaseGrinxException):
    def __init__(self, location: str):
        super().__init__(
            exception_code=404,
            user_readable_message='Not Found',
            content=bytes(f'Location not found {location}', 'utf8'),
        )

