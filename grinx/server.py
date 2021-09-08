import asyncio
from asyncio import StreamReader, StreamWriter

from configuration.cli_builder import CommandLineInterfaceBuilder


async def request_handler(reader: StreamReader, writer: StreamWriter):
    data = await reader.read(1024)
    writer.write(b"HTTP/1.1 200 OK\r\n")
    writer.write(b"Content-Length: 1\r\n")
    writer.write(b"Content-Type: text/html\r\n")
    writer.write(b"Accept-Ranges: bytes\r\n")
    writer.write(b"\r\n")
    writer.write(b"1")
    await writer.drain()


async def main(args):
    server = await asyncio.start_server(request_handler, args.host, args.port, )
    print(server.sockets[0].getsockname())
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    parser = CommandLineInterfaceBuilder().build()
    args = parser.parse_args()
    asyncio.run(main(args))
