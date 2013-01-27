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
        def add(*args):
            return reduce(operator.add, args)

        with environment(func=add) as env:
            with READ("(func 1 2)") as sexp:
                assert lisp_eval(sexp, env) == 3
            with READ("(func 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6
            with READ("(func 1 (func 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 5

    def test_eval_builtin_add(self):
        with environment() as env:
            with READ("(+ 1 2)") as sexp:
                assert lisp_eval(sexp, env) == 3
            with READ("(+ 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6
            with READ("(+ 1 (+ 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 5

    def test_eval_builtin_sub(self):
        with environment() as env:
            with READ("(- 1 2)") as sexp:
                assert lisp_eval(sexp, env) == -1
            with READ("(- 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == -4
            with READ("(- 1 (- 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 1

    def test_eval_builtin_mul(self):
        with environment() as env:
            with READ("(* 2 2)") as sexp:
                assert lisp_eval(sexp, env) == 4
            with READ("(* 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6
            with READ("(* 1 (* 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 4

    def test_eval_predicates(self):
        with environment() as env:
            with READ("(number? 3)") as sexp:
                assert lisp_eval(sexp, env) == True
            with READ("(number? 3.5)") as sexp:
                assert lisp_eval(sexp, env) == True

# vim: set ft=python ts=4 sw=4 expandtab :

