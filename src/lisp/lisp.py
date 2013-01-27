# -*- coding: utf-8 -*-
#
# Copyright (c) Stefan Eletzhofer
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import sys
import types
import logging

from exc import ReaderError
from exc import EvaluatorError

from env import Frame

from evaluator import lisp_eval
from reader import lisp_read
from printer import lisp_print

logger = logging.getLogger("lisp.lisp")


def setup_logging(level=logging.DEBUG):
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")


def main():
    setup_logging()
    environment = Frame.global_frame()
    while True:
        try:
            inp = raw_input(">>> ")
        except EOFError:
            break
        try:
            print lisp_print(lisp_eval(lisp_read(inp), environment))
        except ReaderError, e:
            print "reader error: " + str(e)
        except EvaluatorError, e:
            print "error evaluating: " + str(e)

if __name__ == '__main__':
    main()

# vim: set ft=python ts=4 sw=4 expandtab :
