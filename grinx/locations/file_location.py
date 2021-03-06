import abc
import logging
import mimetypes
import os.path
from abc import ABC

from grinx.exceptions.not_found import GrinxNotFoundException
from grinx.locations.base import BaseLocation
from grinx.requests import BaseRequest
from grinx.responses import BaseResponse
from grinx.responses.files_responses import ListDirectoryResponse, FileContentResponse
from grinx.open_files_cache import OpenFilesCache

logger = logging.getLogger()
FILE_CACHE = OpenFilesCache()


class BaseFileLocation(BaseLocation, ABC):
    def __init__(self, path_starts_with: str, file_cache=FILE_CACHE):
        self.path_starts_with = path_starts_with
        self.file_cache = file_cache

    async def process_request(self, request_to_process: BaseRequest) -> BaseResponse:
        logger.debug(f"processing location {request_to_process.path} with FILE location")

        path_to_file = self.get_full_path_to_file(request_to_process.path)

        if not self.check_os_path_goes_only_deep(path_to_file):
            raise GrinxNotFoundException(path_to_file)

        response = await self.get_response_for_path_to_file(path_to_file, request_to_process.path)
        return response

    def check_if_appropriate_for_request(self, request: BaseRequest) -> bool:
        return request.path.startswith(self.path_starts_with)

    @abc.abstractmethod
    def get_full_path_to_file(self, request_uri: str) -> str:
        ...

    async def get_response_for_path_to_file(self, path_to_file: str, request_path_to_append: str) -> BaseResponse:
        if not os.path.exists(path_to_file):
            raise GrinxNotFoundException(path_to_file)

        if os.path.isdir(path_to_file):
            files = os.listdir(path_to_file)

            correct_paths = [os.path.join(request_path_to_append, f) for f in files]
            return ListDirectoryResponse.create_with_files_list_as_content(correct_paths)

        guessed_type, encoding = mimetypes.guess_type(path_to_file)

        if guessed_type and 'text' not in guessed_type:
            mode = 'rb'
        else:
            mode = 'r'

        f = await self.file_cache.open(path_to_file, mode, encoding)

        content = await f.readlines()

        if mode == 'r':
            if encoding is None:
                encoding = 'utf-8'
            content_as_bytes = bytes(''.join(content), encoding)
        else:
            content_as_bytes = b''.join(content)
        return FileContentResponse.create_with_file_content(content_as_bytes, guessed_type, encoding)

    @staticmethod
    def get_path_without_leading_slash(path_to_proceed: str) -> str:
        return path_to_proceed[1:]

    @abc.abstractmethod
    def check_os_path_goes_only_deep(self, path_to_file: str):
        ...


class RootFileLocation(BaseFileLocation):
    def __init__(self, path_starts_with: str, root: str):
        super().__init__(path_starts_with)
        self.root = root

    def get_full_path_to_file(self, request_uri: str) -> str:
        return os.path.join(self.root, self.remove_path_starts_with(request_uri))

    def check_os_path_goes_only_deep(self, path_to_file: str) -> bool:
        return os.path.commonpath([self.root, path_to_file]) == self.root

    def remove_path_starts_with(self, request_uri: str) -> str:
        return request_uri.split(self.path_starts_with)[1]


class AliasFileLocation(BaseFileLocation):
    def __init__(self, path_starts_with: str, alias: str):
        super().__init__(path_starts_with)
        self.alias = alias

    def get_full_path_to_file(self, request_uri: str) -> str:
        removed_location_stars_with = request_uri.split(self.path_starts_with)[1]
        return os.path.join(self.alias, self.get_path_without_leading_slash(removed_location_stars_with))

    def check_os_path_goes_only_deep(self, path_to_file: str):
        return os.path.commonpath([self.alias, path_to_file]) == self.alias


__all__ = (
    'RootFileLocation',
    'AliasFileLocation',
)
