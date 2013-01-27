import unittest

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

# vim: set ft=python ts=4 sw=4 expandtab :

