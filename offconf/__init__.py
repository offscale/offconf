#!/usr/bin/env python

from base64 import b64encode, b64decode
from os import environ, path
from itertools import takewhile

__author__ = "Samuel Marks"
__version__ = "0.0.5"

funcs = {
    "b64encode": b64encode,
    "b64decode": b64decode,
    "takewhile": takewhile,
    "prepend": lambda pre: lambda s: "{pre}{s}".format(s=s, pre=pre),
    "append": lambda app: lambda s: "{s}{app}".format(s=s, app=app),
    "int": int,
    "float": float,
    "str": str,
    "dict": dict,
    "list": list,
    "set": set,
    "frozenset": frozenset,
}


def replace_variables(input_s, variables=None, extra_env=None, extra_funcs=None):
    """
    Replace variables like ${foo} with matching from `variables`. Also works with environment variables ${env.bar}.
    Now handles piping to given functions and, custom arrow functions also.

    :param input_s: input string
    :type input_s: `str|unicode`
    :param variables: context of variables
    :type variables: `dict`
    :param extra_env: extra environment variables
    :type extra_env: `dict`
    :param extra_funcs: dictionary of functions, currently just used for pipes `|`
    :type extra_funcs: `dict`

    :return parsed string
    :rtype `str`
    """
    assert isinstance(input_s, str)

    # Linters complain when default arg set to `{}`
    variables = variables or {}  # type: dict
    extra_env = extra_env or {}  # type: dict

    if extra_funcs is not None:
        funcs.update(extra_funcs)

    if len(input_s) < 3:
        return input_s

    environ.update(extra_env)

    parsed_string = ""  # type: str
    possible_var = ""  # type: str

    # Scanner
    for c in input_s:
        if c == "$":
            possible_var += c
        elif len(possible_var) == 1 and c != "{":
            parsed_string += possible_var + c
            possible_var = ""
        elif c == "}" and possible_var:
            possible_var += c
            var = possible_var[len("${") : -len("}")]
            parsed_string += "{}".format(
                (
                    (
                        lambda res: res.replace(path.sep, path.sep + path.sep)
                        if path.sep == "\\"
                        else res
                    )(environ.get(var[len("env.") :], ""))
                    or possible_var
                )
                if var.startswith("env.")
                else pipe(var, funcs)
                if "|" in var
                else variables.get(var, possible_var)
            )
            possible_var = ""
        elif possible_var:
            possible_var += c
        else:
            parsed_string += c

    return parsed_string


parse = replace_variables  # will deprecate `replace_variables` at some point


def pipe(variables, functions):
    """
    Pipe 1 variable through 1-n functions

    >>> pipe('foo|b64encode|b64decode|b64encode', {'b64encode': b64encode, 'b64decode': b64decode})
    Zm9v

    :param variables: context of variables
    :type variables: `str`
    :param functions: dictionary of functions, currently just used for pipes `|`
    :type functions: `dict`

    :return parsed string
    :rtype `str`
    """
    return reduce(
        lambda g, f: f(g),
        (get_func(functions, s.strip(), s) for s in variables.split("|")),
    )


def get_func(functions, expr, val_on_fail):
    probable_f = ""
    parsed_functions = []
    for c in expr:
        if c == "(" and probable_f:
            parsed_functions.append(
                arrow_to_lambda(probable_f)
                if "=>" in probable_f
                else functions[probable_f]
            )
            probable_f = ""
        else:
            probable_f += c
    if "=>" in probable_f:
        parsed_functions.append(arrow_to_lambda(probable_f))
        probable_f = None

    return (
        (
            parsed_functions[0](probable_f.translate(None, "()'\""))
            if probable_f
            else parsed_functions[0]
        )
        if parsed_functions
        else functions.get(probable_f, probable_f) or val_on_fail
    )


def arrow_to_lambda(arrow):
    """
    Evaluate arrow string as lambda function

    >>> arrow_to_lambda('(a,b) => a*b')(5,58)
    290

    :param arrow: arrow function
    :type arrow: `str`

    :return evaluated function
    :rtype `lambda`
    """
    # TODO: Security sanitisation and/or opting this behind a boolean flag. `arrow_to_lambda((a,b) => exit(5))` @ LOL
    return eval(
        "lambda {new_f}".format(new_f=arrow[1:].replace(")", "", 1).replace("=>", ":"))
    )
