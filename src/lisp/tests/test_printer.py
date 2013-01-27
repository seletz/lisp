import unittest

from  lisp.exc import *
from  lisp.printer import *


class TestPrint(unittest.TestCase):

    def test_print_number(self):
        assert print_number(4) == "4"
        assert print_number(4.0) == "4.0"

    def test_print_string(self):
        assert print_string("ff") == "ff"

    def test_print_bool(self):
        assert print_bool(True) == "#t"
        assert print_bool(False) == "#f"

    def test_print_symbol(self):
        assert print_symbol(Symbol("foo")) == "#foo"

    def test_print_list(self):
        assert print_list((Symbol("foo"), 1, 4.3, True)) == "'(#foo 1 4.3 #t)"

