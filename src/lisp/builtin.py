# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
import types
import logging

logger = logging.getLogger("lisp.builtin")


car = lambda x: x and x[0] or None
cdr = lambda x: x and x[1:] or None
cons = lambda a, b: b and (a,b) or (a)
empty = lambda x: x == ()
list_p = lambda x: type(x) == types.TupleType
func_p = callable

# vim: set ft=python ts=4 sw=4 expandtab :
