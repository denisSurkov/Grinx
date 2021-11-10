import abc
import logging
import mimetypes
import os.path
from abc import ABC

import aiofiles

from grinx.exceptions.not_found import GrinxFileNotFoundException
from grinx.locations.base import BaseLocation
from grinx.requests import BaseRequest
from grinx.responses import BaseResponse
from grinx.responses.files_responses import ListDirectoryResponse, FileContentResponse

logger = logging.getLogger()


class BaseFileLocation(BaseLocation, ABC):
    def __init__(self, path_starts_with: str):
        self.path_starts_with = path_starts_with

    async def process_request(self, request_to_process: BaseRequest) -> BaseResponse:
        logger.debug(f"processing location {request_to_process.path} with FILE location")

        path_to_file = self.get_full_path_to_file(request_to_process.path)

        if not self.check_os_path_goes_only_deep(path_to_file):
            raise GrinxFileNotFoundException(path_to_file)

        response = await self.get_response_for_path_to_file(path_to_file, request_to_process.path)
        return response

    def check_if_appropriate_for_request(self, request: BaseRequest) -> bool:
        return request.path.startswith(self.path_starts_with)

    @abc.abstractmethod
    def get_full_path_to_file(self, request_uri: str) -> str:
        ...

    async def get_response_for_path_to_file(self, path_to_file: str, request_path_to_append: str) -> BaseResponse:
        if not os.path.exists(path_to_file):
            raise GrinxFileNotFoundException(path_to_file)

        if os.path.isdir(path_to_file):
            files = os.listdir(path_to_file)

            correct_paths = [os.path.join(request_path_to_append, f) for f in files]
            return ListDirectoryResponse.create_with_files_list_as_content(correct_paths)

        async with aiofiles.open(path_to_file, 'r', encoding='utf8') as f:
            content = await f.readlines()

        guessed_type, encoding = mimetypes.guess_type(path_to_file)
        content_as_bytes = bytes(''.join(content), 'utf8')
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
        return os.path.join(self.root, self.get_path_without_leading_slash(request_uri))

    def check_os_path_goes_only_deep(self, path_to_file: str) -> bool:
        return os.path.commonpath([self.root, path_to_file]) == self.root


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
