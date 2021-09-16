import pytest

from grinx.responses.base import BaseResponse


@pytest.fixture
def response() -> BaseResponse:
    return BaseResponse(200, 'OK')


@pytest.fixture
def basic_writer(mocker):
    return mocker.Mock()


def test_base_response_default_fields():
    response = BaseResponse(200, 'OK')

    assert response.status_code == 200
    assert response.status_message == 'OK'
    assert response.protocol == 'HTTP/1.1'
    assert response.encoding == 'utf8'
    assert response.content is None
    assert response.headers is None


@pytest.mark.parametrize('status_code,status_message,protocol,expected_str', (
    (200, 'OK', 'HTTP/1.1', 'HTTP/1.1 200 OK'),
    (400, 'Wrong Request', 'HTTP/2.0', 'HTTP/2.0 400 Wrong Request'),
))
def test_response_as_str(status_code, status_message, protocol, expected_str):
    response = BaseResponse(status_code, status_message, protocol=protocol)

    assert str(response) == expected_str
