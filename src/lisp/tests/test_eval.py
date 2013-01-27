import unittest
import contextlib

from  lisp.exc import *
from  lisp.env import *
from  lisp.reader import *
from  lisp.evaluator import *


@contextlib.contextmanager
def READ(s):
    sexp = lisp_read(s)
    yield sexp


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

    def test_eval_list(self):
        import operator
        with environment(func=operator.add) as env:
            with READ("(func 1 2)") as sexp:
                assert lisp_eval(sexp, env) == 3


# vim: set ft=python ts=4 sw=4 expandtab :

