import unittest

from  lisp.exc import *
from  lisp.evaluator import *


class TestEnv(unittest.TestCase):

    def get_one(self, parent=None, **kw):
        return Frame(parent=parent, **kw)

    def test_lookup(self):
        """
        test environment lookup.
        """
        with self.assertRaises(EvaluatorError):
            self.get_one().lookup("x")
            self.get_one(x=1).lookup("y")

        assert self.get_one(x=42).lookup("x") == 42

        root = self.get_one(x=42)
        assert self.get_one(parent=root).lookup("x") == 42
        assert self.get_one(parent=root, x=43).lookup("x") == 43

    def test_set(self):
        """
        test setting var values in a env.
        """
        root = self.get_one(x=42)

        assert self.get_one(parent=root).set("y", 1).lookup("y") == 1
        assert self.get_one(parent=root).set("y", 1).lookup("x") == 42
        assert self.get_one(parent=root).set("x", 1).lookup("x") == 1

# vim: set ft=python ts=4 sw=4 expandtab :

