# -*- coding: utf-8 -*-
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import sys
import logging

logger = logging.getLogger("lisp.exceptions")

class EvaluatorError(RuntimeError):
    pass

class ReaderError(RuntimeError):
    pass

# vim: set ft=python ts=4 sw=4 expandtab :
