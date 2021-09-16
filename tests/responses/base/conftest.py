import pytest

from grinx.responses.base import BaseResponse


@pytest.fixture
def response() -> BaseResponse:
    return BaseResponse(200, 'OK')


@pytest.fixture
def response_with_headers() -> BaseResponse:
    return BaseResponse(200, 'OK', headers={
            'Content-Type': 'text/html',
            'Server': 'grinx',
    })


@pytest.fixture
def response_with_content() -> BaseResponse:
    return BaseResponse(200, 'OK', content=b'test content')


@pytest.fixture
def basic_writer(mocker):
    return mocker.Mock()
