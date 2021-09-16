def test_do_nothing_if_no_additional_headers(response, basic_writer):
    response.write_additional_headers(basic_writer)

    basic_writer.assert_not_called()


def test_writes_all_additional_header_with_spaces(response_with_headers, basic_writer, mocker):
    response_with_headers.write_additional_headers(basic_writer)

    basic_writer.assert_has_calls([
        mocker.call(b'Content-Type: text/html'),
        mocker.call(b'\r\n'),
        mocker.call(b'Server: grinx'),
        mocker.call(b'\r\n'),
    ])
