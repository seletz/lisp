# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
import types
import logging
import operator
import functools

logger = logging.getLogger("lisp.builtin")

from reader import Symbol


car      = lambda x: x and x[0] or None
cdr      = lambda x: x and x[1:] or None
cons     = lambda a, b: b and (a,b) or (a)
empty    = lambda x: x == ()

list_p   = lambda x: type(x) == types.TupleType
number_p = lambda x: type(x) in (types.IntType, types.FloatType, types.ComplexType)
string_p = lambda x: type(x) in types.StringTypes
symbol_p = lambda x: isinstance(x, Symbol)
bool_p   = lambda x: isinstance(x, bool)
func_p   = callable

true_p   = lambda x: bool_p(x) and x == True
false_p  = lambda x: not true_p(x)

even_p   = lambda x: x % 2 == 0
odd_p    = lambda x: not even_p(x)

def list_f(*args):
    return tuple(args)

def reduced(f):
    @functools.wraps(f)
    def decorated_function(*args):
        return reduce(f(), args)
    return decorated_function

@reduced
def all_f(*args):
    return operator.and_

@reduced
def some_f(*args):
    return operator.or_

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
