from responses.base import BaseResponse


def test_write_space(basic_writer, mocker):
    BaseResponse.write_space(basic_writer)

    basic_writer.assert_has_calls([
        mocker.call(b'\r\n'),
    ])
