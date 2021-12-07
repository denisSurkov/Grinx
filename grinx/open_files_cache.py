from datetime import datetime, timedelta
from typing import Dict, Tuple
from typing.io import IO

import aiofiles


class OpenFilesCache:
    def __init__(self, valid_time_secs: int = 30):
        self.valid_time_secs = valid_time_secs

        self.open_files: Dict[str, Tuple[IO, datetime]] = dict()

    async def open(self, filepath: str, mode: str, encoding: str) -> IO:
        file, saved_at = self.open_files.get(filepath, (None, None))
        now_time = datetime.now()

        if not file:
            file = await aiofiles.open(filepath, mode, encoding=encoding)
            self.open_files[filepath] = (file, now_time)
            return file

        if saved_at + timedelta(seconds=self.valid_time_secs) < now_time:
            return await self.cache_file_descriptor(filepath, mode, encoding)
        else:
            await file.seek(0)
            return file

    async def cache_file_descriptor(self, filepath: str, mode: str, encoding: str) -> IO:
        now_time = datetime.now()
        file = await aiofiles.open(filepath, mode, encoding=encoding)
        self.open_files[filepath] = (file, now_time)
        return file
