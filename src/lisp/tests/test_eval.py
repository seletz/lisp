import unittest

from  lisp.evaluator import *


class TestEvaluator(unittest.TestCase):

    def test_eval_number(self):
        """
        numbers evaluate to themselves.
        """
        assert lisp_eval(3) == 3
        assert lisp_eval(-3) == -3

# vim: set ft=python ts=4 sw=4 expandtab :

