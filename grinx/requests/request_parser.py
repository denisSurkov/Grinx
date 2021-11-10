import asyncio
from asyncio import StreamReader
from typing import Dict

from exceptions.timeout import GrinxTimeoutException
from grinx.exceptions.bad_request import BadGrinxRequest
from grinx.requests import BaseRequest, RequestPath

ALLOWED_METHOD = frozenset((
    'OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'
))


class RequestParser:
    def __init__(self, reader: StreamReader):
        self.reader = reader

    async def __call__(self) -> BaseRequest:
        return await self.parse_request()

    async def parse_request(self) -> BaseRequest:
        method, path, protocol = await self.parse_first_line()
        headers = await self.parse_headers()

        if method in ('POST', 'PUT'):
            self.check_headers(headers)

        request = BaseRequest.from_header(method, path, protocol, headers)
        request.body = await self.parse_body(request)
        return request

    async def parse_first_line(self) -> (str, RequestPath, str):
        first_line = (await self.read_lines(1))[0].strip()
        split_first_line = first_line.split(' ')

        if len(split_first_line) != 3:
            raise BadGrinxRequest()

        method = split_first_line[0]
        if method not in ALLOWED_METHOD:
            raise BadGrinxRequest('Unknown method')

        uri = split_first_line[1]
        try:
            request_path = RequestPath.from_relative_path(uri)
        except Exception:
            raise BadGrinxRequest('Could not parse URI')

        version = split_first_line[2]
        if version != 'HTTP/1.1':
            print(version)
            raise BadGrinxRequest('Unsupported version')

        return method, request_path, version

    async def parse_headers(self) -> Dict[str, str]:
        raw_header_section = await self.read_until()
        header_lines = raw_header_section.split('\n')[:-1]

        headers = dict()
        for line in header_lines:
            split_line = line.strip().split(':')

            if len(split_line) < 2:
                print(split_line)
                raise BadGrinxRequest('wrong headers')

            header, value = split_line[0], ':'.join(split_line[1:])
            headers[header] = value

        return headers

    async def parse_body(self, request: BaseRequest):
        if request.headers.get('Content-Length') is not None:
            return await self.parse_body_from_content_length(request)

        transfer_encoding = request.headers.get('Transfer-Encoding')

        if transfer_encoding is None:
            return None

        if transfer_encoding != 'chunked':
            raise BadGrinxRequest('Not supported transfer encoding')

        return await self.parse_body_from_chunked(request)

    async def parse_body_from_content_length(self, request: BaseRequest):
        content_length = request.headers['Content-Length']

        if not content_length.isdigit():
            raise BadGrinxRequest('Content length is incorrect')

        bytes_to_read = int(content_length)
        request.body = await self.read_n_bytes(bytes_to_read)

    async def parse_body_from_chunked(self, request: BaseRequest):
        # TODO:
        pass

    @staticmethod
    def check_headers(headers: Dict[str, str]):
        if 'Host' not in headers:
            raise BadGrinxRequest('host not in headers')

        if 'Content-Length' not in headers and 'Transfer-Encoding' not in headers:
            raise BadGrinxRequest('content length and transfer encoding not present')

        if 'Content-Length' in headers and headers.get('Transfer-Encoding') == 'chunked':
            raise BadGrinxRequest('content length and transfer encoding chunked at the same time')

    async def read_lines(self, lines_count: int, timeout: int = 1) -> [str]:
        lines = []
        try:
            for _ in range(lines_count):
                line: bytes = await asyncio.wait_for(self.reader.readline(), timeout=timeout)
                lines.append(line.decode('utf-8'))
        except asyncio.TimeoutError:
            raise GrinxTimeoutException()

        return lines

    async def read_until(self, until: bytes = b'\r\n', timeout=3) -> str:
        try:
            all_before = await asyncio.wait_for(self.reader.readuntil(until), timeout=timeout)
        except asyncio.TimeoutError:
            raise GrinxTimeoutException()
        except asyncio.LimitOverrunError:
            raise BadGrinxRequest('Request is too long')
        except asyncio.IncompleteReadError:
            raise BadGrinxRequest('Wrong format')

        decoded_before = all_before.decode('utf-8')
        return decoded_before

    async def read_n_bytes(self, n_bytes: int, timeout=3):
        try:
            content = await asyncio.wait_for(self.reader.read(n_bytes), timeout=timeout)
        except asyncio.TimeoutError:
            raise GrinxTimeoutException()
        except asyncio.LimitOverrunError:
            raise BadGrinxRequest('Request is too long')
        except asyncio.IncompleteReadError:
            raise BadGrinxRequest('Wrong format')

        decoded_content = content.decode('utf-8')
        return decoded_content
