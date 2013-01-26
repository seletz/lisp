import unittest

from  lisp.reader import lisp_read


class TestRead(unittest.TestCase):

    def test_read_empty_list(self):
        assert lisp_read("()"), "reader returns nothing"
