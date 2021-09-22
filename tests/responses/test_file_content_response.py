from grinx.responses import FileContentResponse


def test_create_with_file_content_correct_return():
    response = FileContentResponse.create_with_file_content(b'important file content')

    assert isinstance(response, FileContentResponse)
    assert response.headers == {'Content-Type': 'text/plain'}
    assert response.status_code == 200
    assert response.status_message == 'OK'
    assert response.content == b'important file content'
