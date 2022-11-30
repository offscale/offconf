# -*- coding: utf-8 -*-

from ast import parse
from distutils.sysconfig import get_python_lib
from functools import partial
from operator import attrgetter, itemgetter
from os import listdir, path
from sys import version_info

from setuptools import find_packages, setup

if version_info[0] == 2:
    from itertools import ifilter as filter
    from itertools import imap as map


def to_funcs(*paths):
    """
    Produce function tuples that produce the local and install dir, respectively.

    :param paths: one or more str, referring to relative folder names
    :type paths: ```*paths```

    :return: 2 functions
    :rtype: ```Tuple[Callable[Optional[List[str]], str], Callable[Optional[List[str]], str]]```
    """
    return (
        partial(path.join, path.dirname(__file__), package_name, *paths),
        partial(path.join, get_python_lib(prefix=""), package_name, *paths),
    )


if __name__ == "__main__":
    package_name = "offconf"

    f_for = partial(path.join, path.dirname(__file__), package_name)
    d_for = partial(path.join, get_python_lib(), package_name)

    samples_join, samples_install_dir = to_funcs("samples")

    with open(path.join(package_name, "__init__.py")) as f:
        __author__, __version__ = map(
            lambda const: const.value if hasattr(const, "value") else const.s,
            map(
                attrgetter("value"),
                map(
                    itemgetter(0),
                    map(
                        attrgetter("body"),
                        map(
                            parse,
                            filter(
                                lambda line: line.startswith("__version__")
                                or line.startswith("__author__"),
                                f,
                            ),
                        ),
                    ),
                ),
            ),
        )

    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        description="Replace variables like `${foo}` within files. Environment variables `${env.bar}`, "
        "handles piping to given functions and, custom arrow functions also.",
        classifiers=[
            "Development Status :: 7 - Inactive",
            "Intended Audience :: Developers",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
            "License :: OSI Approved :: MIT License",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        test_suite=package_name + ".tests",
        packages=find_packages(),
        package_dir={package_name: package_name},
        data_files=[
            (samples_install_dir(), list(map(samples_join, listdir(samples_join()))))
        ],
    )
