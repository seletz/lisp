import unittest

from  lisp.exc import *
from  lisp.printer import *


class TestPrint(unittest.TestCase):

    def test_print_number(self):
        assert print_number(4) == "4"
        assert print_number(4.0) == "4.0"

    def test_print_string(self):
        assert print_string("ff") == "ff"
        assert lisp_print("ff") == "ff"

    def test_print_bool(self):
        assert print_bool(True) == "#t"
        assert print_bool(False) == "#f"
        assert lisp_print((True, False)) == "'(#t #f)"

    def test_print_symbol(self):
        assert print_symbol(Symbol("foo")) == "#foo"

    def test_print_list(self):
        assert print_list((Symbol("foo"), 1, 4.3, True)) == "'(#foo 1 4.3 #t)"

    def test_print_lambda(self):
        l = Lambda(None, None, None)
        assert print_lambda(l) == repr(l)
        assert print_list((l,)) == "'(" + repr(l) +")"

    def test_print_err(self):
        with self.assertRaises(PrinterError):
            print_list(({},))

