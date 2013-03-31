======
lisp
======

:Author:    Stefan Eletzhofer
:Date:      2013-03-31

Abstract
========

This repo contains my take in implementing a lisp in python.

Motivation
==========

Due to lack of education I only recently came across the
famous `SICP`.  To me, this book is both very fascinating
and frustrating at the same time.  So I decided to implement
a lisp in python -- my favourite language -- to better grok
the meaning of lisp.

I'll try to get all the examples in `SICP` running in my
little hack.

Current state
=============

The thing now has:

- basic read-eval-print loop
- basic numerical ops
- define, cond, if, begin, lambda, quote
- nested environments
- functions:
  - and or
- some predicates -- but I guess they're pretty nonstandard:
  - odd? even? list? number? string?

no, NO macros yet.  Also no map, fold, reduce, ... yet.

.. vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
