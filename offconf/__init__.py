#!/usr/bin/env python

from os import environ

__author__ = 'Samuel Marks'
__version__ = '0.0.1'


def replace_variables(input_s, variables=None, extra_env=None):
    """
    Replace variables like ${foo} with matching from `variables`. Also works with environment variables ${env.bar}.

    :arg input_s :type StringType
    :arg variables :type DictType
    :arg extra_env :type DictType

    :return parsed_string :type StringType
    """
    assert isinstance(input_s, basestring)

    variables = variables or {}  # Linters complain when default arg set to `{}`
    extra_env = extra_env or {}  # Linters complain when default arg set to `{}`

    if len(input_s) < 3:
        return input_s

    environ.update(extra_env)

    parsed_string = ''
    possible_var = ''

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
            parsed_string += environ.get(var[len('env.'):], possible_var) \
                if var.startswith('env.') else variables.get(var, possible_var)
            possible_var = ''
        elif possible_var:
            possible_var += c
        else:
            parsed_string += c

    return parsed_string
