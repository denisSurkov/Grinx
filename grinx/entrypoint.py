import asyncio
import logging
from asyncio import StreamReader, StreamWriter
from logging import getLogger

from grinx.configuration.cli_builder import CommandLineInterfaceBuilder
from grinx.request_processor import RequestProcessor

logging.basicConfig(level=logging.DEBUG)

logger = getLogger(__name__)


async def request_handler(reader: StreamReader, writer: StreamWriter):
    logger.debug('Got new request')
    request_processor = RequestProcessor(reader, writer)
    await request_processor()


async def entrypoint(args):
    server = await asyncio.start_server(request_handler, args.host, args.port)
    logger.debug('Starting server on %s', server.sockets[0].getsockname())
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    parser = CommandLineInterfaceBuilder().build()
    args = parser.parse_args()
    asyncio.run(entrypoint(args))
