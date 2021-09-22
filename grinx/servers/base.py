from typing import Tuple

from grinx.locations import BaseLocation
from grinx.requests.base import BaseRequest


class BaseServer:
    def __init__(self, host: str, locations: Tuple[BaseLocation]):
        self.host: str = host
        self.locations = locations

    def check_if_can_accept_request(self, request: BaseRequest) -> bool:
        # TODO: check by host
        return True

    async def process_request(self, request: BaseRequest):
        # TODO: find location for request
        pass
