from asyncio import StreamReader, StreamWriter
from logging import getLogger

logger = getLogger(__name__)


class UnprocessableRequestException(BaseException):
    ...


class Request:
    def __init__(self):
        self.body = b""
        self.method = ""
        self.path = ""
        self.protocol = ""
        self.headers = {

        }

    def __str__(self):
        return f"{self.method} {self.path} {self.protocol}"


class RequestProcessor:
    DEFAULT_READ_SIZE = 1024

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

        self._body = b""
        self._data_read = 0
        self._read_all_data = False
        self._request_working_on = Request()

    async def __call__(self):
        await self.process()

    async def process(self):
        await self.read()

        self.writer.write(b"HTTP/1.1 200 OK\r\n")
        self.writer.write(b"Content-Length: 1\r\n")
        self.writer.write(b"Content-Type: text/html\r\n")
        self.writer.write(b"Accept-Ranges: bytes\r\n")
        self.writer.write(b"\r\n")
        self.writer.write(b"1")
        await self.writer.drain()

    async def read(self):
        data_read = 0
        data_chunk = await self.reader.read(self.DEFAULT_READ_SIZE)
        data_read += self.DEFAULT_READ_SIZE
        self.analyze_data(data_chunk)

    def analyze_data(self, data_chunk: bytes):
        if self._data_read <= self.DEFAULT_READ_SIZE:
            header = self.analyze_header(data_chunk)

    def analyze_header(self, data_chunk: bytes):
        lines = data_chunk.split(b'\r\n')
        first_part = lines[0]

        splited_first_part = first_part.decode('UTF-8').split(' ')
        if len(splited_first_part) != 3:
            raise UnprocessableRequestException('Wrong header')

        method = splited_first_part[0]
        self._request_working_on.method = method

        path = splited_first_part[1]
        self._request_working_on.path = path

        protocol = splited_first_part[2]
        self._request_working_on.protocol = protocol
