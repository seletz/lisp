# -*- coding: utf-8 -*-
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import types
import logging

logger = logging.getLogger("lisp.print")


def print_number(n):
    """
    numbers print verbatim.

    >>> print print_number(7)
    7

    """
    return str(n)


def print_symbol(s):
    """
    symbols print verbatim.

    >>> print print_symbol("x")
    x

    """
    return s


def print_list(lst):
    """
    Lists are printed quoted and recuresively.

    >>> print print_list((1, 2))
    '(1 2)
    >>> print print_list(())
    '()

    """
    return "'(" + " ".join(map(lisp_print, lst)) + ")"


def lisp_print(sexp):
    if type(sexp) == types.TupleType:
        return print_list(sexp)
    else:
        return str(sexp)

# vim: set ft=python ts=4 sw=4 expandtab :
