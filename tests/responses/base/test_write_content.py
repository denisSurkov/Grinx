def test_do_nothing_if_no_content(response, basic_writer):
    response.write_content(basic_writer)

    basic_writer.assert_not_called()


def test_write_content_without_space(response_with_content, basic_writer, mocker):
    response_with_content.write_content(basic_writer)

    basic_writer.assert_has_calls([
            mocker.call(b'test content'),
    ])
