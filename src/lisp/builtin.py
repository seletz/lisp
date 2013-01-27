# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
import logging

logger = logging.getLogger("lisp.builtin")


car = lambda x: x and x[0] or None
cdr = lambda x: x and x[1:] or None
cons = lambda a, b: b and (a,b) or (a)

# vim: set ft=python ts=4 sw=4 expandtab :
