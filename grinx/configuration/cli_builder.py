from argparse import ArgumentParser


class CommandLineInterfaceBuilder:
    def __init__(self):
        self.argument_parser = ArgumentParser(
                prog='Grinx',
                usage='./grinx.py localhost 8080',
                description='Python web server with asyncio',
        )

    def build(self) -> ArgumentParser:
        self.add_required_args()
        self.add_info_about_config_file()

        return self.argument_parser

    def add_required_args(self):
        self.argument_parser.add_argument(
                'host',
                action='store',
                default='localhost',
                help='Host where server will serve, could be IP or localhost',
        )

        self.argument_parser\
            .add_argument(
                'port',
                action='store',
                default=2021,
        )

    def add_info_about_config_file(self):
        self.argument_parser.add_argument(
                '--config-file',
                action='store',
                nargs=1,
                required=False,
        )
