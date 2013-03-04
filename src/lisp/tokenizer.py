# -*- coding: utf-8 -*-
#
# Copyright (c) Stefam Eletzhofer
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import sys
import re
import logging

logger = logging.getLogger("lisp.tokenize")

TOK_PAREN_OPEN  = "TOK_PAREN_OPEN"
TOK_PAREN_CLOSE = "TOK_PAREN_CLOSE"

TOK_QUOTE       = 'TOK_QUOTE'

TOK_STRING      = 'TOK_STRING'
TOK_NUMBER      = 'TOK_NUMBER'
TOK_SYMBOL      = 'TOK_SYMBOL'
TOK_CHAR        = 'TOK_CHAR'
TOK_UNKNOWN     = 'TOK_UNKNOWN'

RX_NUMBER = re.compile("^[+-]?(\d*\.?\d+|\d+\.?\d*)([eE][+-]?\d+)?$")
RX_SYMBOL = re.compile("^([a-zA-Z0-9+-<>=:$\*\?!]+)$")

class TokenizerException(RuntimeError):
    def __init__(self, message, state):
        self.message = message
        self.state = state

class State(object):
    STATE_NONE   = -1
    STATE_STRING = 0
    STATE_SYMBOL = 1
    STATE_CHAR   = 2
    STATE_STRING_CHAR   = 3

    states = {
        STATE_NONE:   "STATE_NONE",
        STATE_STRING: "STATE_STRING",
        STATE_SYMBOL: "STATE_SYMBOL",
        STATE_CHAR:   "STATE_CHAR",
        STATE_STRING_CHAR:   "STATE_STRING_CHAR",
    }

    def __init__(self, index=None, char=None):
        self.index = index
        self.char  = char
        self.state = self.STATE_NONE

    def state_name(self, s):
        return self.states.get(s, "UNKNOWN")

    def set(self, s=STATE_NONE):
        logger.debug("STATE %s -> %s" % (self.state_name(self.state), self.state_name(s)))
        self.state = s

    @property
    def is_string(self):
        return self.state == self.STATE_STRING

    @property
    def is_symbol(self):
        return self.state == self.STATE_SYMBOL

    @property
    def is_char(self):
        return self.state == self.STATE_CHAR

    @property
    def is_string_char(self):
        return self.state == self.STATE_STRING_CHAR

    def __repr__(self):
        return "TokenizerState state=%s {index=%r, char='%c'}" % (self.state_name(self.state), self.index, self.char)


def tokenize(s):
    s.strip()
    s = s + " "

    state = State()

    tok = ""

    for nr, char in enumerate(s):
        logger.debug("---------------------------------------------------------")
        state.index = nr
        state.char  = char

        logger.debug("tok='%s' state: %r" % (tok, state))

        if state.is_char or state.is_string_char:
            logger.debug("char|string_char")
            the_char = {
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                    }.get(char, char)
            if state.is_string_char:
                char = the_char
                state.set(state.STATE_STRING)
                tok += char
                continue
            else:
                state.set(state.STATE_NONE)
                yield (TOK_CHAR, the_char)
                tok = ""
                continue

        if state.is_string:
            logger.debug("string")
            if char == '"':
                state.set(state.STATE_NONE)
                yield (TOK_STRING, tok)
                tok = ""
                continue
            if char == '\\':
                state.set(state.STATE_STRING_CHAR)
                continue

            tok += char
            continue

        if state.is_symbol:
            logger.debug("symbol")
            if not RX_NUMBER.match(char) and not RX_SYMBOL.match(char):
                if RX_NUMBER.match(tok):
                    yield (TOK_NUMBER, tok)
                elif RX_SYMBOL.match(tok):
                    yield (TOK_SYMBOL, tok)
                else:
                    yield (TOK_UNKNOWN, tok)
                state.set(state.STATE_NONE)
                tok = ""
            else:
                tok += char
                continue

        if char in ' \t\r\n':
            logger.debug("whitespace")
            continue

        if char == '(':
            logger.debug("TOK_PAREN_OPEN")
            yield (TOK_PAREN_OPEN, char)
            continue
        elif char == ')':
            yield (TOK_PAREN_CLOSE, char)
            continue
        elif char == "'":
            yield (TOK_QUOTE, char)
            continue
        elif char == '\\':
            state.set(state.STATE_CHAR)
            continue
        elif char == '"':
            tok = ""
            state.set(state.STATE_STRING)
            continue

        # fall-thru
        if state.state == state.STATE_NONE:
            state.set(state.STATE_SYMBOL)
            tok = tok + char

    if state.is_string:
        raise TokenizerException("unexpected EOF: unterminated string.", state)

    if state.is_symbol:
        raise TokenizerException("unexpected EOF: symbol prematurely ended", state)


if __name__ == '__main__':
    from pprint import pprint
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")
    logger.setLevel(logging.DEBUG)
    while True:
        try:
            s = raw_input(">>> ")
            pprint(tuple(tokenize(s)))
        except TokenizerException, e:
            pprint("Exception: %s state: %r" % (e.message, e.state))


# vim: set ft=python ts=4 sw=4 expandtab :
