# -*- coding: utf-8 -*-
#
# Copyright (c) Stefam Eletzhofer
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import sys
import logging

logger = logging.getLogger("lisp.tokenize")

TOK_PAREN_OPEN  = "("
TOK_PAREN_CLOSE = ")"

def tokenize(s):
    sc = s[:]
    sc.strip()
    sc = sc.replace("(", " ( ").replace(")", " ) ")
    logger.debug("tokenizer: sc=%r" % sc)
    for k in sc.split():
        yield k

# vim: set ft=python ts=4 sw=4 expandtab :
