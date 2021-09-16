def test_write_default_protocol_header(response, basic_writer, mocker):
    response.write_protocol_header(basic_writer)

    basic_writer.assert_has_calls([
            mocker.call(b'HTTP/1.1 200 OK'),
            mocker.call(b'\r\n'),
    ])


def test_write_different_protocol_header(response, basic_writer, mocker):
    response.protocol = 'HTTP/2.0'

    response.write_protocol_header(basic_writer)

    basic_writer.assert_has_calls([
            mocker.call(b'HTTP/2.0 200 OK'),
            mocker.call(b'\r\n'),
    ])


