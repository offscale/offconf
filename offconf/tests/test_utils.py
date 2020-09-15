from unittest import TestCase, main as unittest_main

from offconf import pipe, get_func, funcs


class TestUtils(TestCase):
    expr = "foo|prepend('bar_')|append('_can')"
    expect = "bar_foo_can"

    def test_pipe(self):
        self.assertEqual(pipe("foo|b64encode", funcs), "Zm9v")
        self.assertEqual(pipe(self.expr, funcs), self.expect)

    def test_get_func(self):
        for idx, expr in enumerate(self.expr.split("|")):
            if idx == 0:
                self.assertEqual(get_func(funcs, expr, "null"), "foo")
            else:
                self.assertTrue(callable(get_func(funcs, expr, None)))


if __name__ == "__main__":
    unittest_main()
