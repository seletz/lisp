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

from reader import Symbol
from builtin import *


logger = logging.getLogger("lisp.eval")

__all__ = ["lisp_eval"]


class Lambda(object):
    def __init__(self, args, body, env):
        self.args = args
        self.body = body
        self.env = env

    def __repr__(self):
        return "#Lambda{%d}" % id(self)

def tagged_list(lst, tag):
    """tagged_list(lst, tag) -> boolean

    Returns true if the list has the tag as first item.

    >>> tagged_list((Symbol("foo"), 1, 2), "foo")
    True

    >>> tagged_list((Symbol("foo"), 1, 2), "bar")
    False
    """
    if list_p(lst):
        hd = car(lst)
        if symbol_p(hd):
            return hd.name == tag
    return False

def self_evaluating(exp):
    """self_evaluating(exp) -> boolean

    Returns true if the expression given is self-evaluating.

    >>> self_evaluating(1)
    True
    >>> self_evaluating(1.0)
    True
    >>> self_evaluating(1+3j)
    True
    >>> self_evaluating('"string"')
    True
    """
    if number_p(exp):
        return True
    if string_p(exp):
        return True
    return False

def evaluate_list(lst, env):
    logger.debug("evaluate_list: lst=%r env=%r" %(lst, env))
    if not list_p(lst):
        return lisp_eval(lst, env)
    return map(lambda x: lisp_eval(x, env), lst)

def evaluate_primitive(f, args, env):
    logger.debug("evaluate_primitive: f=%r" % f)
    return f(*evaluate_list(args, env))

def evaluate_apply(lst, env):
    logger.debug("evaluate_apply(lst=%r)" % repr(lst))

    first = car(lst)
    rest  = cdr(lst)

    if list_p(first):
        value = lisp_eval(first, env)
    elif symbol_p(first):
        value = env.lookup(first)
    else:
        raise EvaluatorError("apply: the CAR of the expression is neither a list nor symbol.")

    if isinstance(value, Lambda):
        l = value
        assert len(l.args) == len(rest), "Argument length mismatch: %r" % l
        arg_names = [s.name for s in l.args]
        sub_env = env.new_frame()
        for nr, name in enumerate(arg_names):
            v = lisp_eval(rest[nr], env)
            sub_env.setf(name, v)
        return lisp_eval(l.body, sub_env)

    if func_p(value):
        return evaluate_primitive(value, rest, env)

    raise EvaluatorError("the value of `%s` is not a function." % first)

def evaluate_quote(sexp):
    logger.debug("evaluate_quote: %r" % repr(sexp))
    q = cdr(sexp)
    if len(q) == 1:
        return q[0]
    else:
        return q

def evaluate_define(sexp, env):
    assert len(sexp) == 3
    symbol = sexp[1]
    rest = sexp[2]

    logger.debug("evaluate_define: %r %r" % (repr(symbol), repr(rest)))

    env.define(symbol.name)
    env.set(symbol.name, lisp_eval(rest, env))

    return "ok"

def evaluate_assignment(sexp, env):
    assert len(sexp) == 3
    symbol = sexp[1]
    rest = sexp[2]

    logger.debug("evaluate_assignment: %r %r" % (repr(symbol), repr(rest)))

    env.set(symbol.name, lisp_eval(rest, env))

    return "ok"

def evaluate_lambda(sexp, env):
    """
    (lambda (a b c) (+ a b c))
    """
    assert len(sexp) == 3
    args   = sexp[1]
    body   = sexp[2]

    l = Lambda(args, body, env)
    logger.debug("evaluate_lambda: => %r" % l)
    return l

def evaluate_begin(sexp, env):
    raise NotImplementedError()

def evaluate_if(sexp, env):
    raise NotImplementedError()

def evaluate_cond(sexp, env):
    raise NotImplementedError()

def quoted_p(sexp):
    return tagged_list(sexp, "quote")

def definition_p(sexp):
    return tagged_list(sexp, "define")

def assignment_p(sexp):
    return tagged_list(sexp, "set!")

def lambda_p(sexp):
    return tagged_list(sexp, "lambda")

def if_p(sexp):
    return tagged_list(sexp, "if")

def cond_p(sexp):
    return tagged_list(sexp, "cond")

def begin_p(sexp):
    return tagged_list(sexp, "begin")


def lisp_eval(sexp, env=None):
    logger.debug("eval: sexp=%r env=%r" % (sexp, env))
    if not env:
        env = Frame.global_frame()

    if self_evaluating(sexp):
        return sexp

    elif symbol_p(sexp):
        logger.debug("lookup symbol %r" % sexp)
        return env.lookup(sexp.name)

    elif quoted_p(sexp):
        return evaluate_quote(sexp)

    elif assignment_p(sexp):
        return evaluate_assignment(sexp, env)

    elif definition_p(sexp):
        return evaluate_define(sexp, env)

    elif if_p(sexp):
        return evaluate_if(sexp, env)

    elif lambda_p(sexp):
        return evaluate_lambda(sexp, env)

    elif cond_p(sexp):
        return evaluate_cond(sexp, env)

    elif begin_p(sexp):
        return evaluate_begin(sexp, env)

    elif list_p(sexp):
        return evaluate_apply(sexp, env)

    else:
        raise EvaluatorError("Can't evaluate: %r" % sexp)


# vim: set ft=python ts=4 sw=4 expandtab :
