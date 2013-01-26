import unittest

from  lisp.evaluator import *


class TestEvaluator(unittest.TestCase):

    def test_eval_number(self):
        """
        numbers evaluate to themselves.
        """
        assert lisp_eval(3) == 3
        assert lisp_eval(-3) == -3

    def test_eval_vars(self):
        """
        vars evaluate to their values.
        """
        env = Frame(a=42, b="foo")
        assert lisp_eval("a", env) == 42
        assert lisp_eval("b", env) == "foo"

        with self.assertRaises(EvaluatorError):
            lisp_eval("x", env)


# vim: set ft=python ts=4 sw=4 expandtab :

