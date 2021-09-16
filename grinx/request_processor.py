from asyncio import StreamReader, StreamWriter
from logging import getLogger

from grinx.exceptions.base import BaseGrinxException
from grinx.requests.base import BaseRequest
from grinx.requests.request_parser import RequestParser
from grinx.responses.base import BaseResponse

logger = getLogger(__name__)


class RequestProcessor:
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

        self._body = b""
        self._data_read = 0
        self._read_all_data = False

    async def __call__(self):
        await self.process()

    async def process(self):
        try:
            request: BaseRequest = await self.read()
            response: BaseResponse = self.process_request(request)
        except BaseGrinxException as e:
            response: BaseResponse = e.to_response()

        response.flush_to_writer(self.writer.write)

        await self.writer.drain()
        self.writer.close()

    async def read(self) -> BaseRequest:
        request_parser = RequestParser(self.reader)
        return await request_parser()

    def process_request(self, request: BaseRequest) -> BaseResponse:
        if request.request_uri == '/fail':
            return BaseResponse(400, 'Bad request', content=b'fuck!')
        return BaseResponse(200, 'OK', content=b'not fuck!')