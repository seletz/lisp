# -*- coding: utf-8 -*-
#
# Copyright (c) Stefam Eletzhofer
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import re
import sys
import ast
import types
import logging

from collections import namedtuple

from exc import ReaderError

from tokenizer import *

logger = logging.getLogger("lisp.reader")


class Symbol(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "'" + self.name


def read_number(value):
    logger.debug("read_number: %r" % value)
    return ast.literal_eval(value)


def read_symbol(value):
    logger.debug("read_symbol: %r" % value)
    return Symbol(value)


def read_string(value):
    logger.debug("read_string: %r" % value)
    return value


def lisp_read(s, state=None):
    logger.debug("lisp_read: s=%r" % s)

    if not state:
        state = {
                "stack": []
        }

    stack = state["stack"]

    sexp = []

    for tok, value in tokenize(s):
        if tok == TOK_PAREN_OPEN:
            subexp = []
            stack.append(sexp)
            sexp = subexp

        elif tok == TOK_PAREN_CLOSE:
            if not stack:
                raise ReaderError("unbalanced open paren")

            tmp = stack.pop()
            tmp.append(tuple(sexp))
            sexp = tmp
            logger.debug("lisp_read: pop => %r" % sexp)

        elif tok == TOK_NUMBER:
            sexp.append(read_number(value))

        elif tok == TOK_SYMBOL:
            sexp.append(read_symbol(value))

        elif tok == TOK_STRING:
            sexp.append(read_string(value))

        elif tok == TOK_UNKNOWN:
            if value.lower() == "#t":
                sexp.append(True)
            elif value.lower() == "#f":
                sexp.append(False)
            else:
                raise ReaderError("unknown token: %s value %r" % (tok, value))

        else:
            raise ReaderError("unexpected token: %r" % tok)

    if stack:
        raise ReaderError("missing close paren")

    logger.debug("lisp_read: => %r" % sexp)
    if len(sexp):
        return sexp[0]

    return None

# vim: set ft=python ts=4 sw=4 expandtab :
