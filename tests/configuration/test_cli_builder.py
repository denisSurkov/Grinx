from argparse import ArgumentParser

import pytest

from grinx.configuration.cli_builder import CommandLineInterfaceBuilder


@pytest.fixture()
def built_parser() -> ArgumentParser:
    builder = CommandLineInterfaceBuilder()
    return builder.build()


@pytest.fixture()
def sys_exit_mock(mocker):
    return mocker.patch('argparse._sys.exit')


@pytest.mark.parametrize('args_input', [
    ('', ),
    ('"localhost"',),
    ('2222',),
])
def test_parser_exits_if_no_required_arguments(built_parser: ArgumentParser,
                                               sys_exit_mock,
                                               args_input):
    built_parser.parse_args('')

    sys_exit_mock.assert_called_once_with(2)
