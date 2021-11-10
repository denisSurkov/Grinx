import datetime
import os
from asyncio import StreamReader, StreamWriter
from logging import getLogger
from grinx.requests.base import BaseRequest
from grinx.requests.request_parser import RequestParser
from grinx.responses.base import BaseResponse
from grinx.locations.file_location import RootFileLocation

#
# 10.185.248.71 - - [09/Jan/2015:19:12:06 +0000] 808840 "GET /inventoryService/inventory/purchaseItem?userId=20253471&itemId=23434300 HTTP/1.1" 500 17 "-" "Apache-HttpClient/4.2.6 (java 1.5)"



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
            response: BaseResponse = await self.process_request(request)
        except BaseException as e:
            logger.debug(f"got problem {e}")
            response: BaseResponse = e.to_response()

        self.write_to_log_about_response(self.writer.get_extra_info('peername'), response)
        response.flush_to_writer(self.writer.write)

        await self.writer.drain()
        self.writer.close()

    async def read(self) -> BaseRequest:
        request_parser = RequestParser(self.reader)
        return await request_parser()

    async def process_request(self, request: BaseRequest) -> BaseResponse:
        location = RootFileLocation(path_starts_with='/', root=os.path.join(os.getcwd()))

        if location.check_if_appropriate_for_request(request):
            return await location.process_request(request)
        return BaseResponse(200, 'OK', content=b'not fuck!')

    @staticmethod
    def write_to_log_about_response(peername: str, response: BaseResponse):
        now_date = datetime.datetime.now()
        str_date = now_date.strftime('%d/%b/%Y:%H:%M:%S %z')

        # TODO: get data from request (first line)
        logger.info(f'{peername} - - [{str_date}]')

