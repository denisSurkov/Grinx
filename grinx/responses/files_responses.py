from typing import List, Optional

from grinx.responses import BaseResponse


class ListDirectoryResponse(BaseResponse):
    @classmethod
    def create_with_files_list_as_content(cls, files_paths: List[str]) -> 'ListDirectoryResponse':
        content = cls.generate_dots_for_list(files_paths)
        return ListDirectoryResponse(
            200,
            'OK',
            content,
            headers={
                'Content-Type': 'text/html',
            },
        )

    @staticmethod
    def generate_dots_for_list(files_path: List[str]) -> bytes:
        parts = ['<ul>']

        for path in files_path:
            parts.append('<li>')
            parts.append('<a href="')
            parts.append(path)
            parts.append('">')
            parts.append(path)
            parts.append('</a></li>')

        parts.append('</ul>')
        return bytes(''.join(parts), 'utf8')


class FileContentResponse(BaseResponse):
    @staticmethod
    def create_with_file_content(file_content: bytes,
                                 content_type: Optional[str] = None,
                                 content_encoding: Optional[str] = None) -> 'FileContentResponse':
        if not content_type:
            content_type = 'text/plain'

        headers = dict()
        headers['Content-Type'] = content_type

        if content_encoding:
            headers['Content-Encoding'] = content_encoding

        return FileContentResponse(
                status_code=200,
                status_message='OK',
                content=file_content,
                headers=headers,
        )


__all__ = (
    'ListDirectoryResponse',
    'FileContentResponse',
)
