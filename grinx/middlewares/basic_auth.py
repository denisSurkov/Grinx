from typing import List, Tuple, Optional
from base64 import b64encode

from grinx.exceptions.unauthorized import GrinxUnauthorizedException
from grinx.middlewares.base import BaseMiddleware
from grinx.requests import BaseRequest
from grinx.responses import BaseResponse


class BasicAuthMiddleware(BaseMiddleware):
    DEFAULT_WWW_AUTHNTICATE_STRING = 'Basic realm="User Visible Realm"'

    def __init__(self, allowed_users: List[Tuple[str, str]]):
        self.allowed_users = allowed_users
        self.encoded_users = self.encode_users(allowed_users)

    def new(self) -> 'BaseMiddleware':
        return BasicAuthMiddleware(self.allowed_users)

    @staticmethod
    def encode_users(users: List[Tuple[str, str]]) -> List[str]:
        return list(
                map(lambda p: b64encode(bytes(f'{p[0]}:{p[1]}', 'utf8')).decode('utf8'), users)
        )

    async def process_before(self, request: BaseRequest) -> BaseRequest:
        auth = request.headers.get('Authorization')
        if not auth or 'Basic' not in auth:
            raise GrinxUnauthorizedException(self.DEFAULT_WWW_AUTHNTICATE_STRING)

        basic_split = auth.split('Basic ')[1]
        if basic_split in self.encoded_users:
            return request
        raise GrinxUnauthorizedException(self.DEFAULT_WWW_AUTHNTICATE_STRING)

    async def process_after(self, request: BaseRequest, response: Optional[BaseResponse], any_exception: Optional[BaseException] = None) -> BaseResponse:
        return response
