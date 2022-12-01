# -*- coding: utf-8 -*-

"""
Shared utility functions used by many tests
"""
from functools import partial
from sys import modules, version_info
from unittest import main

if version_info[0] == 2:
    from imp import load_source

    from mock import MagicMock, patch

    def exec_mod_and_return(modname, filepath):
        """
        Execute module, add it to `sys.modules`, and return it

        :param modname: Module name
        :type modname: ```str```

        :param filepath: Filepath
        :type filepath: ```str```

        :return: The module
        """
        modules[modname] = load_source(modname, filepath)
        return modules[modname]

else:
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    from unittest.mock import MagicMock, patch

    def exec_mod_and_return(modname, filepath):
        """
        Execute module, add it to `sys.modules`, and return it

        :param modname: Module name
        :type modname: ```str```

        :param filepath: Filepath
        :type filepath: ```str```

        :return: The module
        """
        loader = SourceFileLoader(
            modname,
            filepath,
        )
        modules[modname] = module_from_spec(spec_from_loader(loader.name, loader))
        loader.exec_module(modules[modname])
        return modules[modname]


def run_cli_test(
    test_case_instance,
    cli_argv,
    exit_code,
    output,
    output_checker=lambda output: (lambda q: output[output.find(q) + len(q) :])(
        "error: "
    ),
    exception=SystemExit,
    return_args=False,
):
    """
    CLI test helper, wraps exit code and stdout/stderr input_str

    :param test_case_instance: instance of `TestCase`
    :type test_case_instance: ```unittest.TestCase```

    :param cli_argv: cli_argv, can be sys.argv or proxy
    :type cli_argv: ```List[str]```

    :param exit_code: exit code
    :type exit_code: ```Optional[int]```

    :param output: string representation (from stdout/stderr)
    :type output: ```Optional[str]```

    :param output_checker: Function to check the input_str with
    :type output_checker: ```Callable[[str], bool]```

    :param exception: The exception that is expected to be raised
    :type exception: ```Union[BaseException, Exception]```

    :param return_args: Primarily use is for tests. Returns the args rather than executing anything.
    :type return_args: ```bool```

    :return: input_str
    :rtype: ```Tuple[str, Optional[Namespace]]```
    """
    argparse_mock, args = MagicMock(), None
    with patch("argparse.ArgumentParser._print_message", argparse_mock), patch(
        "sys.argv", cli_argv
    ):
        from offconf.__main__ import main

        main_f = partial(main, cli_argv=cli_argv, return_args=return_args)
        if exit_code is None:
            args = main_f()
        else:
            with test_case_instance.assertRaises(exception) as e:
                args = main_f()
    if exit_code is not None:
        test_case_instance.assertEqual(
            *(e.exception.code, exception(exit_code).code)
            if exception is SystemExit
            else (str(e.exception), output)
        )
    if exception is not SystemExit:
        pass
    elif argparse_mock.call_args is None:
        test_case_instance.assertIsNone(output)
    else:
        test_case_instance.assertEqual(
            output_checker(
                (
                    argparse_mock.call_args.args
                    if version_info[:2] > (3, 7)
                    else argparse_mock.call_args[0]
                )[0]
            ),
            output,
        )
    return output, args


def unittest_main():
    """Runs unittest.main if __main__"""
    if __name__ == "__main__":
        main()


__all__ = ["exec_mod_and_return", "run_cli_test", "unittest_main"]
