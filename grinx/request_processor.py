import datetime
from asyncio import StreamReader, StreamWriter
from logging import getLogger
from typing import Dict, Any, Optional, List

from grinx.exceptions.not_found import GrinxNotFoundException
from grinx.requests.base import BaseRequest
from grinx.requests.request_parser import RequestParser
from grinx.responses.base import BaseResponse
from grinx.servers.base import BaseServer

logger = getLogger(__name__)


class RequestProcessor:
    SERVERS: List[BaseServer] = []

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

        self.log_bag: Dict[str, Any] = dict()
        self.log_bag['peername'] = self.writer.get_extra_info('peername', ('unkown', '0'))
        self.log_bag['received_at'] = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')

    async def __call__(self):
        await self.process()

    async def process(self):
        client_asks_for_keep_alive = True
        should_just_close = False
        count_response = 0

        while client_asks_for_keep_alive:
            try:
                request: BaseRequest = await self.read()
                response: BaseResponse = await self.process_request(request)
                client_asks_for_keep_alive = request.headers.get('Connection', '').strip() == 'keep-alive'
            except BaseException as e:
                if count_response > 0:
                    client_asks_for_keep_alive = False
                    should_just_close = True

                logger.debug(f"got problem {e}")
                response: BaseResponse = e.to_response()

            self.log_bag['response_code'] = response.status_code
            self.log_bag['body_len'] = len(response.content) if response.content else 0

            if not should_just_close:
                self.write_to_log_about_response()
                response.flush_to_writer(self.writer.write)

            count_response += 1
            if not should_just_close:
                await self.writer.drain()

        self.writer.close()

    async def read(self) -> BaseRequest:
        request_parser = RequestParser(self.reader, self.log_bag)
        return await request_parser()

    async def process_request(self, request: BaseRequest) -> BaseResponse:
        server_to_process: Optional[BaseServer] = None
        for server in self.SERVERS:
            if server.check_if_can_accept_request(request):
                server_to_process = server

        if not server_to_process:
            raise GrinxNotFoundException(request.path)

        return await server_to_process.process_request(request)

    def write_to_log_about_response(self):
        peername = self.log_bag.get('peername')
        client = f'{peername[0]}:{peername[1]}'

        recevied_at = self.log_bag.get('received_at')
        first_line = self.log_bag.get('first_line')
        status_code = self.log_bag.get('response_code')
        body_len = self.log_bag.get('body_len')

        logger.info(f'{client} - - [{recevied_at}] "{first_line}" {status_code} {body_len}')

