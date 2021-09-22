import abc
from typing import Awaitable

from grinx.requests import BaseRequest
from grinx.responses import BaseResponse


class BaseLocation(abc.ABC):
    @abc.abstractmethod
    async def process_request(self, request_to_process: BaseRequest) -> Awaitable[BaseResponse]:
        ...

    @abc.abstractmethod
    def check_if_appropriate_for_request(self, request: BaseRequest) -> bool:
        ...
