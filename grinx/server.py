import asyncio
import logging
from asyncio import StreamReader, StreamWriter
from logging import getLogger

from configuration.cli_builder import CommandLineInterfaceBuilder
from request_processor import RequestProcessor

logging.basicConfig(level=logging.DEBUG)

logger = getLogger(__name__)


async def request_handler(reader: StreamReader, writer: StreamWriter):
    logger.debug('got new request')
    request_processor = RequestProcessor(reader, writer)
    await request_processor()


async def main(args):
    server = await asyncio.start_server(request_handler, args.host, args.port, )
    logger.debug('strating server on %s', server.sockets[0].getsockname())
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    parser = CommandLineInterfaceBuilder().build()
    args = parser.parse_args()
    asyncio.run(main(args))
