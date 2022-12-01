#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from json import loads

from offconf import __description__, __version__, parse


def _build_parser():
    """
    Build parser

    :return parser object
    :rtype `ArgumentParser`
    """
    parser = ArgumentParser(description=__description__, prog="python -m offconf")
    parser.add_argument("-f", "--filename", help="Input file", required=True)
    parser.add_argument("-o", "--output-file", help="Output file", required=True)
    parser.add_argument(
        "-v", "--variables", help="Any variables to be interpolated (as JSON string)"
    )
    parser.add_argument(
        "-e",
        "--env-variables",
        help="Any environment variables to be interpolated (as JSON string)",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    return parser


def main(cli_argv=None, return_args=False):
    """
    Run the CLI parser

    :param cli_argv: CLI arguments. If None uses `sys.argv`.
    :type cli_argv: ```Optional[List[str]]```

    :param return_args: Primarily use is for tests. Returns the args rather than executing anything.
    :type return_args: ```bool```

    :return: the args if `return_args`, else None
    :rtype: ```Optional[Namespace]```
    """
    _parser = _build_parser()
    args = _parser.parse_args(args=cli_argv)

    with open(args.filename) as f:
        input_s = f.read()

    if args.variables:
        args.variables = loads(args.variables)
    if args.env_variables:
        args.env_variables = loads(args.env_variables)

    output_s = parse(input_s, variables=args.variables, extra_env=args.env_variables)

    with open(args.output_file, "w") as f:
        f.write(output_s)


if __name__ == "__main__":
    main()

__all__ = ["main"]
