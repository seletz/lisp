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

from exc import EvaluatorError
from env import Frame
from builtin import *

logger = logging.getLogger("lisp.eval")

__all__ = ["lisp_eval"]


def evaluate_func(f, args, env):
    logger.debug("evaluate_func: f=%r" % f)
    return f(*map(lambda x: lisp_eval(x, env), args))


def evaluate_list(lst, env):
    logger.debug("evaluate_list(lst=%r" % repr(lst))

    first = car(lst)
    rest  = cdr(lst)

    func = env.lookup(first)
    if func_p(func):
        return evaluate_func(func, rest, env)

    f = env.lookup(car(lst))
    if not func_p(f):
        raise EvaluatorError("the value of `%s` is not a function." % car(lst))



def lisp_eval(sexp, env=None):
    if not env:
        env = Frame.global_frame()
    if type(sexp)  == types.TupleType:
        return evaluate_list(sexp, env)
    else:
        if type(sexp) in types.StringTypes:
            return env.lookup(sexp)

    return sexp

# vim: set ft=python ts=4 sw=4 expandtab :
