import os.path

import pytest

from grinx.requests import BaseRequest, RequestPath
from grinx.locations import RootFileLocation


@pytest.mark.parametrize('root_path, request_path, expected_full_os_path', [
    (os.path.join('some', 'path'), '/foo', os.path.join('some', 'path', 'foo')),
    (os.path.join('some', 'path'), '/foo/file', os.path.join('some', 'path', 'foo', 'file')),
])
def test_full_path_to_file_from_request(root_path, request_path, expected_full_os_path):
    location = RootFileLocation(path_starts_with='/', root=root_path)

    assert location.get_full_path_to_file(request_path) == expected_full_os_path


@pytest.mark.parametrize('file_location_starts_with, request_path, expected', [
        ('/', '/any/path/', True),
        ('/', '/', True),
        ('/special-path/', '/not-special-path/', False),
        ('/special-path/', '/special-path/too', True),
        ('/special-path/', '/special-path/too/too', True),
])
def test_check_if_appropriate_for_request(file_location_starts_with, request_path, expected):
    request = BaseRequest(method='GET', request_path=RequestPath(request_path))
    file_location = RootFileLocation(path_starts_with=file_location_starts_with, root='/some/path/')

    assert file_location.check_if_appropriate_for_request(request) is expected


# TODO: add tests for get response for file

