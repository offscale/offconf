#!/usr/bin/env python
from __future__ import print_function
from base64 import b64encode, b64decode
from os import environ, path

__author__ = 'Samuel Marks'
__version__ = '0.0.3'


def replace_variables(input_s, variables=None, extra_env=None, extra_funcs=None):
    """
    Replace variables like ${foo} with matching from `variables`. Also works with environment variables ${env.bar}.

    :param input_s: input string
    :type input_s: `str`
    :param variables: context of variables
    :type variables: `dict`
    :param extra_env: extra environment variables
    :type extra_env: `dict`
    :param funcs: dictionary of functions, currently just used for pipes `|`
    :type funcs: `dict`

    :return parsed string
    :rtype `str`
    """
    assert isinstance(input_s, basestring)

    # Linters complain when default arg set to `{}`
    variables = variables or {}  # type: dict
    extra_env = extra_env or {}  # type: dict
    funcs = {'b64encode': b64encode, 'b64decode': b64decode}
    if extra_funcs is not None:
        funcs.update(extra_funcs)

    if len(input_s) < 3:
        return input_s

    environ.update(extra_env)

    parsed_string = ''  # type: str
    possible_var = ''  # type: str

    # Scanner
    for c in input_s:
        if c == '$':
            possible_var += c
        elif len(possible_var) == 1 and c != '{':
            parsed_string += possible_var + c
            possible_var = ''
        elif c == '}' and possible_var:
            possible_var += c
            var = possible_var[len('${'):-len('}')]
            parsed_string += ((lambda res: res.replace(path.sep, path.sep + path.sep) if path.sep == '\\' else res
                               )(environ.get(var[len('env.'):], '')) or possible_var) \
                if var.startswith('env.') else pipe(var, funcs) if '|' in var else variables.get(var, possible_var)
            possible_var = ''
        elif possible_var:
            possible_var += c
        else:
            parsed_string += c

    return parsed_string


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
    return reduce(lambda g, f: f(g), (functions.get(s.strip(), s) for s in variables.split('|')))
