from grinx.exceptions.base import BaseGrinxException


class GrinxUnauthorizedException(BaseGrinxException):
    def __init__(self, auth_type_string: str):
        super().__init__(
                exception_code=401,
                user_readable_message='Unauthorized',
                headers={
                    'WWW-Authenticate': auth_type_string,
                },
        )
