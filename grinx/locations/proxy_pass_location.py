import aiohttp

from grinx.exceptions.bad_request import BadGrinxRequest
from grinx.locations.base import BaseLocation
from grinx.requests import BaseRequest
from grinx.responses import BaseResponse


class ProxyPassLocation(BaseLocation):
    def __init__(self, path_starts_with: str, pass_to_address: str):
        self.path_starts_with = path_starts_with
        self.pass_to_address = pass_to_address

    async def process_request(self, request_to_process: BaseRequest) -> BaseResponse:
        headers_copy = {k: v for k, v in request_to_process.headers.items()}
        headers_copy['Host'] = self.get_new_host()

        try:
            async with aiohttp.ClientSession() as session:
                response = await session.request(request_to_process.method,
                                                 self.get_rewritten_url(request_to_process),
                                                 headers=headers_copy,
                                                 data=request_to_process.body)
                converted_response = await self.convert_from_aiohttp_response_to_grinx_response(response)
                return converted_response
        except BaseException as e:
            raise BadGrinxRequest(str(e))

    def check_if_appropriate_for_request(self, request: BaseRequest) -> bool:
        return request.path.startswith(self.path_starts_with)

    async def convert_from_aiohttp_response_to_grinx_response(self, response: aiohttp.ClientResponse) -> BaseResponse:
        content, _ = await response.content.readchunk()

        correct_headers = dict()
        for h in response.headers:
            if h == 'Connection' or h == 'Transfer-Encoding' or h == 'Content-Encoding':
                continue
            correct_headers[h] = response.headers[h]

        return BaseResponse(response.status, response.reason, content, correct_headers)

    def get_rewritten_url(self, request: BaseRequest) -> str:
        return f'{self.pass_to_address}{request.full_path}'

    def get_new_host(self) -> str:
        return self.pass_to_address.split('http://')[1]
