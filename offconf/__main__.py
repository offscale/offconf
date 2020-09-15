#!/usr/bin/env python

from argparse import ArgumentParser
from json import loads

from .__init__ import replace_variables


def _build_parser():
    """
    Build parser

    :return parser object
    :rtype `ArgumentParser`
    """
    parser = ArgumentParser(description="Interpolate variables from file")
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
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()

    with open(args.filename) as f:
        input_s = f.read()

    if args.variables:
        args.variables = loads(args.variables)
    if args.env_variables:
        args.env_variables = loads(args.env_variables)

    output_s = replace_variables(
        input_s, variables=args.variables, extra_env=args.env_variables
    )

    with open(args.output_file, "w") as f:
        f.write(output_s)
