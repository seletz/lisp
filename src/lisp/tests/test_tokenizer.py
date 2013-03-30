import unittest

from  lisp.tokenizer import *
from  lisp.lisp import setup_logging
from  lisp.lisp import lisp_read


class TestTokenizer(unittest.TestCase):

    def test_tokenize_empty(self):
        assert tokenize("")

    def test_tok_empty_list(self):
        assert tokenize("()")
        assert list(tokenize("()")) == [(TOK_PAREN_OPEN, "("), (TOK_PAREN_CLOSE, ")")]

    def test_tok_string(self):
        assert list(tokenize('("foo")')) == [(TOK_PAREN_OPEN, "("), (TOK_STRING, "foo"), (TOK_PAREN_CLOSE, ")")]
        assert list(tokenize('("\\"hello\\"")')) == [(TOK_PAREN_OPEN, "("), (TOK_STRING, '"hello"'), (TOK_PAREN_CLOSE, ")")]

    def test_tok_char(self):
        tokens = list(tokenize('\\t'))
        assert tokens[0][0] == TOK_CHAR
        assert tokens[0][1] == '\t'
