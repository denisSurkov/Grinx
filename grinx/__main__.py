import asyncio
import logging
from asyncio import StreamReader, StreamWriter
from logging import getLogger

from grinx.configuration.config_parser import ConfigParser
from grinx.configuration.cli_builder import CommandLineInterfaceBuilder
from grinx.request_processor import RequestProcessor
from grinx.open_files_cache import OpenFilesCache

logging.basicConfig(level=logging.INFO, format='%(msg)s')

logger = getLogger(__name__)


async def request_handler(reader: StreamReader, writer: StreamWriter):
    logger.debug('Got new request')
    request_processor = RequestProcessor(reader, writer)
    await request_processor()


async def entrypoint(config_parser_):
    server = await asyncio.start_server(request_handler, config_parser_.host, config_parser_.port)
    logger.debug('Starting server on %s', server.sockets[0].getsockname())
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    parser = CommandLineInterfaceBuilder().build()
    args = parser.parse_args()

    cache = OpenFilesCache()
    config_parser = ConfigParser(args.config)
    RequestProcessor.SERVERS = config_parser.configure_servers()

    try:
        asyncio.run(entrypoint(config_parser))
    except KeyboardInterrupt:
        exit()
