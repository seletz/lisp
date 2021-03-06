import unittest

from  lisp.exc import *
from  lisp.reader import Symbol
from  lisp.reader import lisp_read


class TestRead(unittest.TestCase):

    def test_read_number(self):
        assert lisp_read("42")     == 42
        assert lisp_read("-42")    == -42
        assert lisp_read(".3")     == .3
        assert lisp_read("-1.3e2") == -130

    def test_read_symbol(self):
        assert lisp_read("a")     == Symbol("a")
        assert lisp_read("foo?")  == Symbol("foo?")
        assert lisp_read("*out*") == Symbol("*out*")
        assert lisp_read("set!")  == Symbol("set!")

    def test_read_string(self):
        assert lisp_read("\"foo\"") == 'foo'
        assert lisp_read("\" abc foo\"") == ' abc foo'

    def test_read_empty_list(self):
        assert lisp_read("()") == ()

    def test_read_list(self):
        assert lisp_read("(foo 1 2)") == ( Symbol("foo"), 1, 2)
        assert lisp_read("(foo (1 2))") == ( Symbol("foo"), (1, 2))

    def test_unexpected_token(self):
        with self.assertRaises(ReaderError):
            lisp_read(".foo")

    def test_unexpected_token(self):
        with self.assertRaises(ReaderError):
            lisp_read("(1 2 3")
