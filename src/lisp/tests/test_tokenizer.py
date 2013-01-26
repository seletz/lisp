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


