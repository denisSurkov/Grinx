import pytest

from grinx.responses.files_responses import ListDirectoryResponse


@pytest.mark.parametrize('files_list, expected_bytes', [
    (['file1'], b'<ul><li><a href="file1">file1</a></li></ul>'),
    ([], b'<ul></ul>'),
    (['file1', 'file2'], b'<ul><li><a href="file1">file1</a></li>'
                         b'<li><a href="file2">file2</a></li></ul>'),
])
def test_generate_dots_for_list(files_list, expected_bytes):
    dots_list = ListDirectoryResponse.generate_dots_for_list(files_list)

    assert isinstance(dots_list, bytes)
    assert dots_list == expected_bytes


def test_create_with_files_list_as_content():
    response = ListDirectoryResponse.create_with_files_list_as_content(['file1', 'file2'])

    assert isinstance(response, ListDirectoryResponse)
    assert response.headers == {'Content-Type': 'text/html'}
    assert response.status_code == 200
    assert response.status_message == 'OK'
    assert response.content == b'<ul><li><a href="file1">file1</a></li>'\
                               b'<li><a href="file2">file2</a></li></ul>'
