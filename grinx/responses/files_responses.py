from typing import List

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
        # возможно, это бред писать так на питоне.
        # я предположил, что так будет быстрее
        # но это сильно влияет на читаемость. Этакий StringBuilder
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
    def create_with_file_content(file_content: bytes) -> 'FileContentResponse':
        return FileContentResponse(
                status_code=200,
                status_message='OK',
                content=file_content,
                headers={
                        'Content-Type': 'text/plain',
                })


__all__ = (
    'ListDirectoryResponse',
    'FileContentResponse',
)
