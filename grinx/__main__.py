import asyncio

from grinx.configuration.cli_builder import CommandLineInterfaceBuilder
from grinx.entrypoint import entrypoint

if __name__ == '__main__':
    parser = CommandLineInterfaceBuilder().build()
    args = parser.parse_args()
    asyncio.run(entrypoint(args))
