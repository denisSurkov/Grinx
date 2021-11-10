from abc import ABC, abstractmethod
from typing import Optional

from grinx.requests import BaseRequest
from grinx.responses import BaseResponse


class BaseMiddleware(ABC):
    @abstractmethod
    def new(self) -> 'BaseMiddleware':
        ...

    @abstractmethod
    async def process_before(self, request: BaseRequest) -> BaseRequest:
        ...

    @abstractmethod
    async def process_after(self, request: BaseRequest, response: Optional[BaseResponse], any_exception: Optional[BaseException] = None) -> BaseResponse:
        ...
