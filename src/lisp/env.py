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
import contextlib

from exc import *
from builtin import *

logger = logging.getLogger("lisp.env")

class Frame(object):
    GLOBALS = None

    def __init__(self, parent=None, **kw):
        self.parent = parent
        self.env = kw
        logger.debug("NEW %r" % self)

    def set(self, var, value):
        """set(var, value) -> frame

        Sets the var as holding the value given in this frame.  Returns
        the frame object itself for chaining.

        >>> Frame().set("x", 1).set("y", 2)
        Frame<...>: parent=0 {'y': 2, 'x': 1}

        :returns: frame
        """
        logger.debug("Frame(%d).set: %s <= %r" % (id(self), var, value))
        self.env[var] = value
        return self

    def lookup(self, var):
        """lookup(var) -> value

        Looks up a var in this frame and all parent frames.

        >>> Frame(x=42).lookup("x")
        42
        >>> Frame(x=42).new_frame(y=1).lookup("y")
        1
        >>> Frame(x=42).new_frame(y=1).lookup("x")
        42

        :returns: value
        """
        if var in self.env:
            value = self.env[var]
            logger.debug("Frame(%d).lookup: %s => %r" % (id(self), var, value))
            return value

        if self.parent:
            logger.debug("Frame(%d).lookup: %s => lookup in parent" % (id(self), var))
            return self.parent.lookup(var)

        print "Lookup Error. Frame dump (innermost first):"
        print self
        raise EvaluatorError("lookup of var '%s' failed." % var)

    def new_frame(self, **kw):
        """new_frame() -> object

        Returns a new frame which has this frame als parent frame.

        :returns: frame instance
        """
        return Frame(parent=self, **kw)

    @classmethod
    def global_frame(cls):
        """global_frame() -> object

        Returns or creates the global frame.

        >>> Frame.GLOBALS is None
        True
        >>> Frame.global_frame()
        Frame<...>: parent=0 {}

        :returns: frame instance
        """
        if not cls.GLOBALS:
            glob = cls.GLOBALS = Frame()
            glob.set("car", car)
            glob.set("cdr", cdr)
            glob.set("cons", cons)
            glob.set("+", lambda args: reduce(operator.add, args))
            glob.set("-", lambda args: reduce(operator.sub, args))
            glob.set("*", lambda args: reduce(operator.mul, args))

        return cls.GLOBALS

    def __repr__(self):
        return "Frame<%d>: parent=%d %r" % (id(self), self.parent and id(self.parent) or 0, self.env)

    def __str__(self):
        """
        __str__() -> string

        Returns a string representing a frame stack:

        >>> print Frame()
        Frame<...>: parent=0 {}

        If the frame has parent frames, they're all visited recursively:

        >>> print Frame(x=42).new_frame(y=1)
        Frame<...>: parent=... {'y': 1}
        Frame<...>: parent=0 {'x': 42}

        """
        out = []
        out.append(repr(self))
        if self.parent:
            out.append(str(self.parent))
        return "\n".join(out)


@contextlib.contextmanager
def environment(parent=None, **kw):
    """environment

    A context manager for environments:

    >>> with environment(x=1) as env:
    ...     print env.lookup("x")
    1

    """
    if parent:
        env = parent.new_frame(**kw)
    else:
        env = Frame(**kw)

    yield env

    del env

# vim: set ft=python ts=4 sw=4 expandtab :
