import pytest

from grinx.request_processor import RequestProcessor


@pytest.fixture
def correct_http_bytes_chunk() -> bytes:
    return b"GET / HTTP/1.1\r\n"


@pytest.fixture
def request_processor() -> RequestProcessor:
    # noinspection PyTypeChecker
    return RequestProcessor(None, None)


@pytest.mark.parametrize('input_chunk', [
    b'',
    b'\r\n',
    b'GET 1 1\r\n',
    b'WRONG_OPTION 1 1\r\n',
    b'GET s 1\r\n',
])
def test_analyze_header_raises_exception_if_wrong_header(request_processor, input_chunk):
    with pytest.raises(Exception):
        request_processor.analyze_header(input_chunk)
