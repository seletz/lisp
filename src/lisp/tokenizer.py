# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

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
