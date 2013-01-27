import unittest

from  lisp.exc import *

from  lisp.env import Frame
from  lisp.env import environment


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

        assert self.get_one(parent=root).define("y") # .set("y", 1).lookup("y") == 1
        assert self.get_one(parent=root).define("y").set("y", 1).lookup("x") == 42
        assert self.get_one(parent=root).define("x").set("x", 1).lookup("x") == 1

    def test_new_frame(self):
        """
        test getting a new child frame.
        """
        root = self.get_one(x=42)
        assert root.new_frame().parent
        assert root.new_frame().parent == root
        assert root.new_frame(x=43).lookup("x") == 43

    def test_str(self):
        """
        """
        root = self.get_one(x=42)
        chld = root.new_frame()

        assert str(root)
        assert str(chld)

    def test_context_mgr(self):
        with environment(x=1) as env:
            assert env.parent is Frame.GLOBALS
            assert env.lookup("x") == 1

        with environment(parent=self.get_one(x=42), x=1) as env:
            assert env.parent
            assert env.lookup("x") == 1


# vim: set ft=python ts=4 sw=4 expandtab :

