
# -*- coding: utf-8 -*-
#
# File: .py
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

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

from tokenizer import *

logger = logging.getLogger("lisp.reader")

RX_NUMBER = re.compile("^[+-]?(\d*\.?\d+|\d+\.?\d*)([eE][+-]?\d+)?$")
RX_SYMBOL = re.compile("^(\w+)$")

class ReaderError(RuntimeError):
    pass

def read_list(tokens):
    logger.debug("read_list: %r" % tokens)
    sexp = []

    sexp.append(lisp_read(tok))

    logger.debug("read_list: => %r" % str(tuple(sexp)))
    return tuple(sexp)

def read_number(token):
    logger.debug("read_number: %r" % token)
    return ast.literal_eval(token)

def read_symbol(token):
    logger.debug("read_symbol: %r" % token)
    return token

class ReaderState(object):
    def __init__(self):
        self.stack = []

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
            sexp.append(subexp)
            stack.append(sexp)
            sexp = subexp
        elif tok == TOK_PAREN_CLOSE:
            if not stack:
                raise ReaderError("unbalanced open paren")

            sexp = tuple(stack.pop())

        elif RX_NUMBER.match(tok):
            sexp.append(read_number(tok))
        elif RX_SYMBOL.match(tok):
            sexp.append(read_symbol(tok))
        else:
            raise ReaderError("unexpected token: %r" % tok)

    if stack:
        raise ReaderError("missing close paren")

    logger.debug("lisp_read: => %r" % sexp[0])
    r = sexp[0]
    if type(r) is types.ListType:
        return tuple(r)
    return r

# vim: set ft=python ts=4 sw=4 expandtab :
