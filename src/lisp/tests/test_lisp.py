import unittest

from  lisp.tokenizer import *
from  lisp.lisp import setup_logging
from  lisp.lisp import lisp_read


class TestTokenizer(unittest.TestCase):

    def test_tokenize_empty(self):
        assert tokenize("")

    def test_tokenize_empty_list(self):
        assert tuple(tokenize("( )")) == (TOK_PAREN_OPEN, TOK_PAREN_CLOSE)
        assert tuple(tokenize(" ( ) ")) == (TOK_PAREN_OPEN, TOK_PAREN_CLOSE)
        assert tuple(tokenize("()")) == (TOK_PAREN_OPEN, TOK_PAREN_CLOSE)


class TestRead(unittest.TestCase):

    def test_read_number(self):
        assert lisp_read("42") == 42
        assert lisp_read("-42") == -42
        assert lisp_read(".3") == .3
        assert lisp_read("-1.3e2") == -130

    def test_read_symbol(self):
        assert lisp_read("a") == "a"

    def test_read_empty_list(self):
        assert lisp_read("()") == ()

    def test_read_list(self):
        assert lisp_read("(foo 1 2)") == ( "foo", 1, 2)
        assert lisp_read("(foo (1 2))") == ( "foo", (1, 2))
