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


RX_NUMBER = re.compile("^[+-]?(\d*\.?\d+|\d+\.?\d*)([eE][+-]?\d+)?$")
RX_STRING = re.compile('^"(.*?)"$')
RX_SYMBOL = re.compile("^([a-zA-Z0-9+-:$\*\?!]+)$")


class Symbol(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "#Symbol{" + self.name + "}"


def read_number(token):
    logger.debug("read_number: %r" % token)
    return ast.literal_eval(token)


def read_symbol(token):
    logger.debug("read_symbol: %r" % token)
    return Symbol(token)


def read_string(token):
    logger.debug("read_string: %r" % token)
    return RX_STRING.match(token).groups()[0]


def lisp_read(s, state=None):
    logger.debug("lisp_read: s=%r" % s)

    if not state:
        state = {
                "stack": []
        }

    stack = state["stack"]

    sexp = []

    for tok in tokenize(s):
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

        elif RX_NUMBER.match(tok):
            sexp.append(read_number(tok))

        elif RX_SYMBOL.match(tok):
            sexp.append(read_symbol(tok))

        elif RX_STRING.match(tok):
            sexp.append(read_string(tok))

        elif tok.lower() == "#t":
            sexp.append(True)

        elif tok.lower() == "#f":
            sexp.append(False)

        else:
            raise ReaderError("unexpected token: %r" % tok)

    if stack:
        raise ReaderError("missing close paren")

    logger.debug("lisp_read: => %r" % str(sexp[0]))
    return sexp[0]

# vim: set ft=python ts=4 sw=4 expandtab :
