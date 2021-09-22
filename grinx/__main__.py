import asyncio

from configuration.cli_builder import CommandLineInterfaceBuilder
from entrypoint import entrypoint

if __name__ == '__main__':
    parser = CommandLineInterfaceBuilder().build()
    args = parser.parse_args()
    asyncio.run(entrypoint(args))
