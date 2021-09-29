from typing import Awaitable

from grinx.locations import BaseLocation
from grinx.requests import BaseRequest
from grinx.responses import BaseResponse


class ProxyPassLocation(BaseLocation):
    def __init__(self, path_starts_with: str, pass_to_address: str):
        self.path_starts_with = path_starts_with
        self.pass_to_address = pass_to_address

    async def process_request(self, request_to_process: BaseRequest) -> Awaitable[BaseResponse]:
        # TODO: можно ли юзать requests?
        pass

    def check_if_appropriate_for_request(self, request: BaseRequest) -> bool:
        return request.request_uri.startswith(self.path_starts_with)
