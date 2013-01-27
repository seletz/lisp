# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
import types
import logging
import operator
import functools

logger = logging.getLogger("lisp.builtin")


car = lambda x: x and x[0] or None
cdr = lambda x: x and x[1:] or None
cons = lambda a, b: b and (a,b) or (a)
empty = lambda x: x == ()
list_p = lambda x: type(x) == types.TupleType
func_p = callable

def list_f(*args):
    return tuple(args)

def reduced(f):
    @functools.wraps(f)
    def decorated_function(*args):
        return reduce(f(), args)
    return decorated_function

@reduced
def add_f(*args):
    return operator.add

@reduced
def sub_f(*args):
    return operator.sub

@reduced
def mul_f(*args):
    return operator.mul

@reduced
def div_f(*args):
    return operator.div

# vim: set ft=python ts=4 sw=4 expandtab :
