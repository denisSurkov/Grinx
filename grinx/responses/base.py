from typing import Callable, NoReturn, Optional, Dict

AbstractWriter = Callable[[bytes], NoReturn]


class BaseResponse:
    def __init__(self,
                 status_code: int, status_message: str,
                 content: Optional[bytes] = None,
                 headers: Optional[Dict[str, str]] = None,
                 protocol: str = 'HTTP/1.1',
                 encoding: str = 'utf8'):
        self.status_code = status_code
        self.status_message = status_message
        self.content = content
        self.headers = headers
        self.protocol = protocol
        self.encoding = encoding

    def flush_to_writer(self, writer: AbstractWriter):
        self.write_protocol_header(writer)
        self.write_additional_headers(writer)
        self.write_space(writer)
        self.write_content(writer)

    def write_protocol_header(self, writer: AbstractWriter):
        header = bytes(f'{self.protocol} {self.status_code} {self.status_message}', self.encoding)
        self.write_with_space(header, writer)

    def write_additional_headers(self, writer: AbstractWriter):
        if not self.headers:
            return

        for header in self.headers:
            header_as_bytes = bytes(f'{header}: {self.headers[header]}', self.encoding)
            self.write_with_space(header_as_bytes, writer)

    def write_content(self, writer: AbstractWriter):
        if not self.content:
            return

        writer(self.content)

    @classmethod
    def write_with_space(cls, data: bytes, writer: AbstractWriter):
        writer(data)
        cls.write_space(writer)

    @classmethod
    def write_space(cls, writer: AbstractWriter):
        writer(b'\r\n')

    def __str__(self):
        return f'{self.protocol} {self.status_code} {self.status_message}'
