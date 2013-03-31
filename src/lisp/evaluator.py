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
import functools

from exc import EvaluatorError
from env import Frame

from reader import Symbol
from builtin import *


logger = logging.getLogger("lisp.eval")

__all__ = ["lisp_eval"]

def log_return(f):
    @functools.wraps(f)
    def decorated_function(*args, **kw):
        try:
            val = f(*args, **kw)
            logger.debug("*** %s => %r" % (f.func_name, val))
            return val
        except:
            logger.error("Exception in %s" % (f.func_name))
            raise
    return decorated_function


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
    if bool_p(exp):
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

@log_return
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
    """
    (define symbol expr)
    or
    (define (name args..) body)
    """
    assert len(sexp) == 3, "define needs a symbol and a expression"

    value = None
    if symbol_p(sexp[1]):
        symbol = sexp[1]
        rest = sexp[2]
        logger.debug("evaluate_define: %r %r" % (repr(symbol), repr(rest)))
        value = lisp_eval(rest, env)

    elif list_p(sexp[1]):
        symbol = car(sexp[1])
        args = cdr(sexp[1])
        body = sexp[2]
        value = evaluate_lambda(("lambda", args, body), env)
    else:
        raise EvaluatorError("define: need (define name expr) or (define (name args..) body)")

    env.define(symbol.name)
    env.set(symbol.name, value)

    return "ok"

def evaluate_assignment(sexp, env):
    """
    (set! x expr)
    """
    assert len(sexp) == 3, "set! needs a symbol and a expression"
    symbol = sexp[1]
    rest = sexp[2]

    logger.debug("evaluate_assignment: %r %r" % (repr(symbol), repr(rest)))

    env.set(symbol.name, lisp_eval(rest, env))

    return "ok"

@log_return
def evaluate_lambda(sexp, env):
    """
    (lambda (a b c) (+ a b c))
    """
    assert len(sexp) == 3, "lambda form needs a argument list and a body"
    args   = sexp[1]
    body   = sexp[2]

    l = Lambda(args, body, env)  # XXX: need to clone env for real closure
    logger.debug("evaluate_lambda: => %r" % l)
    return l

@log_return
def evaluate_begin(sexp, env):
    """
    (begin expr expr expr ...)
    """
    values = map(lambda expr: lisp_eval(expr, env), cdr(sexp))
    return values[-1]

@log_return
def evaluate_if(sexp, env):
    """
    (if pred conseq alternative)
    """
    assert len(sexp) >= 3, "if form needs a predicate, a consequence and one optional alternative"
    pred = sexp[1]
    cons = sexp[2]
    if len(sexp) == 4:
        alt  = sexp[3]
    else:
        alt = None

    pred_val = lisp_eval(pred, env)
    if true_p(pred_val):
        return lisp_eval(cons, env)
    else:
        if alt:
            return lisp_eval(alt, env)

    return False

@log_return
def evaluate_cond(sexp, env):
    """
    (cond
        (pred1 expr expr ...)
        (pred2 expr expr ...)
        ...
        (else  expr expr ...)
        )
    """
    logger.debug("evaluate_cond: sexp=%r, env=%r" % (sexp, env))
    assert len(sexp) > 1, "cond with no clauses?"
    clauses = sexp[1:]

    for clause in clauses:
        pred = car(clause)
        expressions = cdr(clause)
        if symbol_p(pred) and pred.name == "else":
            return map(lambda expr: lisp_eval(expr, env), expressions)[-1]

        if true_p(lisp_eval(pred, env)):
            return map(lambda expr: lisp_eval(expr, env), expressions)[-1]

@log_return
def evaluate_or(sexp, env):
    """
    (or expr1 expr2 ...)
    """
    logger.debug("evaluate_or: sexp=%r, env=%r" % (sexp, env))
    if len(sexp) <= 1: raise EvaluatorError("empty or")

    for expr in cdr(sexp):
        value = lisp_eval(expr, env)
        if true_p(value):
            return value

    return value

@log_return
def evaluate_and(sexp, env):
    """
    (and expr1 expr2 ...)
    """
    logger.debug("evaluate_and: sexp=%r, env=%r" % (sexp, env))
    if len(sexp) <= 1: raise EvaluatorError("empty and")

    for expr in cdr(sexp):
        value = lisp_eval(expr, env)
        if false_p(value):
            return value

    return value

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

def or_p(sexp):
    return tagged_list(sexp, "or")

def and_p(sexp):
    return tagged_list(sexp, "and")

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

    elif or_p(sexp):
        return evaluate_or(sexp, env)

    elif and_p(sexp):
        return evaluate_and(sexp, env)

    elif list_p(sexp):
        return evaluate_apply(sexp, env)

    else:
        raise EvaluatorError("Can't evaluate: %r" % sexp)


# vim: set ft=python ts=4 sw=4 expandtab :
