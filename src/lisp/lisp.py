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
import pdb, sys, traceback

from exc import ReaderError
from exc import EvaluatorError

from env import Frame

from evaluator import lisp_eval
from reader import lisp_read
from printer import lisp_print

logger = logging.getLogger("lisp.lisp")


def setup_logging(level=logging.INFO):
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s")

    #logging.getLogger("lisp.reader").setLevel(logging.INFO)
    #logging.getLogger("lisp.env").setLevel(logging.INFO)
    #logging.getLogger("lisp.tokenize").setLevel(logging.INFO)
    #logging.getLogger("lisp.eval").setLevel(logging.INFO)
    #logging.getLogger("lisp.eval").setLevel(logging.INFO)


def eval(sexp, env=None):
    if not env:
        env = Frame.global_frame()

    sexp = lisp_eval(sexp, env)
    s = lisp_print(sexp)
    return s


def main():
    setup_logging()
    environment = Frame.global_frame()
    intr = 0
    should_stop = False
    while not should_stop:
        inp = ""
        prompt = ">>> "
        complete = False
        while not complete:
            try:
                inp = inp + raw_input(prompt)
            except EOFError:
                break
            except KeyboardInterrupt:
                inp = ""
                print "INTR", intr
                if intr:
                    should_stop = True
                intr += 1

            try:
                sexp = lisp_read(inp)
                complete = True
            except ReaderError, e:
                prompt = "... "

        if sexp is None:
            continue

        try:
            print eval(sexp, environment)
            intr = 0
        except EvaluatorError, e:
            print "error evaluating: " + str(e)
            print "sexp:", sexp
            pdb.post_mortem()
        except Exception, e:
            print "exception: " + repr(e)
            print "sexp:", sexp
            pdb.post_mortem()

if __name__ == '__main__':
    main()

# vim: set ft=python ts=4 sw=4 expandtab :
