from argparse import ArgumentParser


class CommandLineInterfaceBuilder:
    def __init__(self):
        self.argument_parser = ArgumentParser(
                prog='Grinx',
                usage='python3 -m grinx /full/path/to/config.json',
                description='Python web server with asyncio',
        )

    def build(self) -> ArgumentParser:
        self.add_required_args()
        return self.argument_parser

    def add_required_args(self):
        self.argument_parser.add_argument(
                'config',
                action='store',
                type=str,
                help='Config for servers',
        )
