import unittest

from  lisp.tokenizer import *

class TestTokenizer(unittest.TestCase):

    def test_tokenize_empty(self):
        assert tokenize("")

    def test_tokenize_empty_list(self):
        assert tuple(tokenize("( )")) == (TOK_PAREN_OPEN, TOK_PAREN_CLOSE)
        assert tuple(tokenize(" ( ) ")) == (TOK_PAREN_OPEN, TOK_PAREN_CLOSE)
        assert tuple(tokenize("()")) == (TOK_PAREN_OPEN, TOK_PAREN_CLOSE)

    def test_tok_long(self):
        assert len(list(tokenize("( 1 2 3)"))) == 5
        assert len(list(tokenize("(a (b c))"))) == 7

# vim: set ft=python ts=4 sw=4 expandtab : 
