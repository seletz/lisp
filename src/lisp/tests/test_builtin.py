import unittest

from  lisp.reader import Symbol
from  lisp.builtin import *

class TestBuiltins(unittest.TestCase):

    def test_car(self):
        assert car((1,2,3)) == 1
        assert car(()) == None

    def test_cdr(self):
        assert cdr((1,2,3)) == (2,3)
        assert cdr(()) == None

    def test_cons(self):
        assert cons(1,2) == (1,2)
        assert cons(1,(3,4)) == (1,(3,4))
        assert cons((),2) == ((),2)
        assert cons(1, ()) == (1)

    def test_pred(self):
        assert empty(()) == True
        assert empty((1,)) == False

        assert list_p((1,)) == True
        assert list_p(()) == True
        assert list_p(1) == False

        assert func_p(1) == False
        assert func_p(lambda x: x) == True

        assert number_p(1) == True
        assert number_p(1.0) == True
        assert number_p(1+3j) == True

        assert string_p("foo") == True
        assert string_p(u"foo") == True

        assert symbol_p(Symbol("a"))

        assert odd_p(3) == True
        assert even_p(2) == True

    def test_reducers(self):
        assert add_f(1,2,3) == 6
        assert sub_f(1,2,3) == -4
        assert mul_f(1,2,3,4) == 24
        assert div_f(4.0,2,2) == 1

    def test_unary_reducer(self):
        assert add_f(1) == 1
        assert sub_f(1) == -1
        assert mul_f(1) == 1
        assert div_f(1) == 1

# vim: set ft=python ts=4 sw=4 expandtab :

