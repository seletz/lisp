# -*- coding: utf-8 -*-
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import types
import logging

from exc import *
from builtin import *
from reader import Symbol
from evaluator import Lambda

logger = logging.getLogger("lisp.print")

lambda_p = lambda x: isinstance(x, Lambda)


def print_number(n):
    """
    numbers print verbatim.

    >>> print print_number(7)
    7

    """
    assert number_p(n)
    return str(n)

def print_string(s):
    """
    strings print verbatim.

    >>> print print_string("a")
    a

    """
    assert string_p(s)
    return str(s)

def print_bool(n):
    """
    strings print verbatim.

    >>> print print_bool(True)
    #t
    >>> print print_bool(False)
    #f

    """
    assert bool_p(n)
    return n and "#t" or "#f"

def print_symbol(s):
    """
    symbols print verbatim.

    >>> print print_symbol(Symbol("x"))
    #x

    """
    assert symbol_p(s)
    return "#" + s.name

def print_func(s):
    """
    funcs print verbatim.

    >>> print print_func(lambda x: x)
    #Func{...}

    """
    assert func_p(s)
    return "#Func{" + repr(s) + "}"

def print_lambda(s):
    assert lambda_p(s)
    return repr(s)

def print_list(lst):
    """
    Lists are printed quoted and recuresively.

    >>> print print_list((1, 2))
    '(1 2)
    >>> print print_list(())
    '()

    """
    logger.debug("print_list: %s" % repr(lst))
    assert list_p(lst)
    return "'(" + " ".join(map(lisp_print, lst)) + ")"


def lisp_print(sexp):
    logger.debug("lisp_print: sexp=%s" % repr(sexp))
    if list_p(sexp):
        return print_list(sexp)
    elif symbol_p(sexp):
        return print_symbol(sexp)
    elif number_p(sexp):
        return print_number(sexp)
    elif bool_p(sexp):
        return print_bool(sexp)
    elif string_p(sexp):
        return print_string(sexp)
    elif func_p(sexp):
        return print_func(sexp)
    elif lambda_p(sexp):
        return print_lambda(sexp)
    else:
        raise PrinterError("Don't know how to print: %r" % (type(sexp)))

# vim: set ft=python ts=4 sw=4 expandtab :
