from responses.base import BaseResponse


def test_write_with_space(basic_writer, mocker):
    BaseResponse.write_with_space(b'some data with space', basic_writer)

    basic_writer.assert_has_calls([
        mocker.call(b'some data with space'),
        mocker.call(b'\r\n'),
    ])
