# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import sys
import logging

from exc import *

logger = logging.getLogger("lisp.env")

class Frame(object):
    GLOBALS = None

    def __init__(self, parent=None, **kw):
        self.parent = parent
        self.env = kw
        logger.debug("NEW %r" % self)

    def set(self, var, value):
        logger.debug("Frame(%d).set: %s <= %r" % (id(self), var, value))
        self.env[var] = value

    def lookup(self, var):
        if var in self.env:
            value = self.env[var]
            logger.debug("Frame(%d).lookup: %s => %r" % (id(self), var, value))
            return value

        if self.parent:
            logger.debug("Frame(%d).lookup: %s => %r" % (id(self), var, value))
            return self.parent.lookup(var)

        print "Lookup Error. Frame dump (innermost first):"
        print self
        raise EvaluatorError("lookup of var '%s' failed." % var)

    def new_frame(self, **kw):
        return Frame(parent=self, **kw)

    @classmethod
    def global_frame(cls):
        if not cls.GLOBALS:
            cls.GLOBALS = Frame()
        return cls.GLOBALS

    def __repr__(self):
        return "Frame<%d>: parent=%d %r" % (id(self), id(self.parent), self.env)

    def __str__(self):
        out = []
        out.append(repr(self))
        if self.parent:
            out.append(str(self.parent))
        return "\n".join(out)

# vim: set ft=python ts=4 sw=4 expandtab :
