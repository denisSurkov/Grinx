import asyncio
from asyncio import StreamReader
from typing import Dict

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

    async def parse_request(self):
        return await self.read_header()

    async def read_header(self):
        first_line = await self.reader.readline()
        splited_first_line = first_line.decode('utf8').strip().split(' ')

        # only three values in first line are allowed
        # so if there are more or less values in first line
        # than server cannot proceed this request
        if len(splited_first_line) != 3:
            raise BadGrinxRequest()

        # https://datatracker.ietf.org/doc/html/rfc2616#section-5.1
        method, request_uri, version = splited_first_line

        self.validate_method(method)
        self.validate_version(version)

        request_path = self.validate_and_parse_request_uri(request_uri)

        callback_to_read_all_headers = self.callback_to_read_all_headers
        callback_to_read_body = self.callback_to_read_all_body

        return BaseRequest.from_header(method, request_path, version)

    def validate_method(self, method: str):
        if method not in ALLOWED_METHOD:
            raise BadGrinxRequest(f'{method} is not allowed')

    def validate_and_parse_request_uri(self, request_uri: str) -> RequestPath:
        return RequestPath.from_relative_path(request_uri)

    def validate_version(self, version: str):
        if version != 'HTTP/1.1':
            raise BadGrinxRequest(f'{version} is not supported')

    def callback_to_read_all_headers(self):
        loop = asyncio.get_running_loop()
        feature = asyncio.run_coroutine_threadsafe(self.reader.readuntil(b'\r\n'), loop)
        result = feature.result()
        return self.parse_headers(result)

    def parse_headers(self, raw_headers: bytes) -> Dict[str, str]:
        decoded_and_splited = raw_headers.decode('utf8').split(' ')

        headers = {}
        for line in decoded_and_splited:
            header, value = map(str.strip, line.split(':'))
            headers[header] = value

        return headers

    def callback_to_read_all_body(self):
        # If a request contains a message-body and a Content-Length is not given,
        # the server SHOULD respond with 400 (bad request) if it cannot determine
        # the length of the message, or with 411 (length required) if it wishes
        # to insist on receiving a valid Content-Length.
        # TODO: ? how to read all body, I have to know headers?
        loop = asyncio.get_running_loop()
        feature = asyncio.run_coroutine_threadsafe(self)

        pass
