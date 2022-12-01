""" Tests for CLI (__main__.py) """

from argparse import ArgumentParser
from sys import version_info
from unittest import TestCase

if version_info[0] == 2:
    pass
else:
    pass

from offconf import __description__, __version__
from offconf.__main__ import _build_parser
from offconf.tests.utils_for_tests import run_cli_test, unittest_main


class TestCli(TestCase):
    """Test class for __main__.py"""

    def test_build_parser(self):
        """Test that `_build_parser` produces a parser object"""
        parser = _build_parser()
        self.assertIsInstance(parser, ArgumentParser)
        self.assertEqual(parser.description, __description__)

    def test_version(self):
        """Tests CLI interface gives version"""
        run_cli_test(
            self,
            ["--version"],
            exit_code=0,
            output=__version__,
            output_checker=lambda output: output[output.rfind(" ") + 1 :][:-1],
        )


unittest_main()
