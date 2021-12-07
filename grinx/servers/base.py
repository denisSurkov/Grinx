from typing import List, Optional

from grinx.exceptions.not_found import GrinxNotFoundException
from grinx.locations.base import BaseLocation
from grinx.requests.base import BaseRequest
from grinx.middlewares.base import BaseMiddleware
from grinx.responses import BaseResponse


class BaseServer:
    def __init__(self, host: str, locations: List[BaseLocation], middlewares: List[BaseMiddleware]):
        self.host: str = host
        self.locations = locations
        self.middlewares = middlewares

    def check_if_can_accept_request(self, request: BaseRequest) -> bool:
        request_host = request.headers.get('Host').strip()
        return request_host == self.host

    async def process_request(self, request: BaseRequest):
        applied_middlewares = await self.apply_middlewares(request)

        appropriate_location = self.find_location(request)

        response = None
        any_exception = None
        try:
            if not appropriate_location:
                raise GrinxNotFoundException(request.path)
            else:
                response = await appropriate_location.process_request(request)
        except BaseException as e:
            any_exception = e

        response_after_reverted_middlewares = await self.revert_middlewares(applied_middlewares, request, response, any_exception)

        if any_exception:
            raise any_exception

        return response_after_reverted_middlewares

    async def apply_middlewares(self, request: BaseRequest) -> List[BaseMiddleware]:
        applied_middlewares = []

        for middleware in self.middlewares:
            middleware_instance = middleware.new()
            request = await middleware_instance.process_before(request)
            applied_middlewares.append(middleware_instance)

        return applied_middlewares

    def find_location(self, request: BaseRequest) -> Optional[BaseLocation]:
        for location in self.locations:
            if location.check_if_appropriate_for_request(request):
                return location
        return None

    async def revert_middlewares(self, applied_middlewares: List[BaseMiddleware],
                                 request: BaseRequest,
                                 response: Optional[BaseResponse],
                                 any_exception: Optional[BaseException] = None) -> BaseResponse:
        for middleware in applied_middlewares[::-1]:
            response = await middleware.process_after(request, response, any_exception)

        return response
