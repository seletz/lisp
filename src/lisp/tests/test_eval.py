import unittest
import contextlib

from  lisp.exc import *
from  lisp.env import *
from  lisp.reader import *
from  lisp.evaluator import *


@contextlib.contextmanager
def READ(s):
    sexp = lisp_read(s)
    yield sexp


@contextlib.contextmanager
def ENV(env=None, **kw):
    if env is None:
        env = Frame.global_frame()

    for k, v in kw.items():
        value = lisp_eval(lisp_read(v), env)
        print "%s <- %r %r" % (k, value, type(value))
        env.setf(k, value)

    yield env

@contextlib.contextmanager
def EVAL(s, **kw):
    with READ(s) as sexp:
        print "SEXP: ", sexp
        with ENV(**kw) as env:
            yield lisp_eval(sexp, env)

class TestEvaluator(unittest.TestCase):

    def test_eval_number(self):
        """
        numbers evaluate to themselves.
        """
        assert lisp_eval(3) == 3
        assert lisp_eval(-3) == -3

    def test_eval_vars(self):
        """
        vars evaluate to their values.
        """
        env = Frame(a=42, b="foo")
        assert lisp_eval(Symbol("a"), env) == 42
        assert lisp_eval(Symbol("b"), env) == "foo"

        with self.assertRaises(EvaluatorError):
            lisp_eval(Symbol("x"), env)

    def test_eval_list(self):
        import operator
        def add(*args):
            return reduce(operator.add, args)

        with environment(func=add) as env:
            with READ("(func 1 2)") as sexp:
                assert lisp_eval(sexp, env) == 3
            with READ("(func 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6
            with READ("(func 1 (func 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 5

    def test_eval_builtin_add(self):
        with environment() as env:
            with READ("(+ 1 2)") as sexp:
                assert lisp_eval(sexp, env) == 3
            with READ("(+ 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6
            with READ("(+ 1 (+ 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 5

    def test_eval_builtin_sub(self):
        with environment() as env:
            with READ("(- 1 2)") as sexp:
                assert lisp_eval(sexp, env) == -1
            with READ("(- 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == -4
            with READ("(- 1 (- 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 1

    def test_eval_builtin_mul(self):
        with environment() as env:
            with READ("(* 2 2)") as sexp:
                assert lisp_eval(sexp, env) == 4
            with READ("(* 1 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6
            with READ("(* 1 (* 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 4

    def test_eval_builtin_and(self):
        with environment() as env:
            with READ("(and #t #t #t)") as sexp:
                assert lisp_eval(sexp, env) == True
            with READ("(and #t #t #f)") as sexp:
                assert lisp_eval(sexp, env) == False
            with READ("(and #f not-evaluated)") as sexp:
                assert lisp_eval(sexp, env) == False

    def test_eval_builtin_or(self):
        with environment() as env:
            with READ("(or #t #t #t)") as sexp:
                assert lisp_eval(sexp, env) == True
            with READ("(or #t #f #f)") as sexp:
                assert lisp_eval(sexp, env) == True
            with READ("(or #f #t not-evaluated)") as sexp:
                assert lisp_eval(sexp, env) == True

    def test_eval_predicates(self):
        with environment() as env:
            with READ("(number? 3)") as sexp:
                assert lisp_eval(sexp, env) == True
            with READ("(number? 3.5)") as sexp:
                assert lisp_eval(sexp, env) == True
            with READ("(string? \"foo\")") as sexp:
                assert lisp_eval(sexp, env) == True

class TestEvalLambda(unittest.TestCase):
    def test_apply(self):
        with environment() as env:
            with READ("((lambda (a b) (* a b)) 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6

    def test_apply_2(self):
        with environment() as env:
            with READ("((lambda (a b) (* a b)) (+ 1 1) (+ 2 2))") as sexp:
                assert lisp_eval(sexp, env) == 8

class TestEvalApply(unittest.TestCase):
    def setUp(self):
        self.env = Frame.global_frame()
        with READ("(define func (lambda (a b) (* a b)))") as sexp:
            lisp_eval(sexp, self.env)

    def test_apply(self):
        with environment(parent=self.env) as env:
            with READ("(func 2 3)") as sexp:
                assert lisp_eval(sexp, env) == 6

class TestIf(unittest.TestCase):
    def setUp(self):
        self.env = Frame.global_frame()
        self.env.setf("a", 2)
        self.env.setf("b", 3)

    def test_if(self):
        with environment(parent=self.env) as env:
            with READ("(if (even? a) #t #f)") as sexp:
                assert lisp_eval(sexp, env) == True
            with READ("(if (even? b) #t #f)") as sexp:
                assert lisp_eval(sexp, env) == False
            with READ("(if (odd? (+ a b)) (+ a b) (- a b))") as sexp:
                assert lisp_eval(sexp, env) == 5
            with READ("(if (odd? (+ a b)) (+ a b))") as sexp:
                assert lisp_eval(sexp, env) == 5

class TestBegin(unittest.TestCase):
    def setUp(self):
        self.env = Frame.global_frame()
        self.env.setf("a", 2)
        self.env.setf("b", 3)

    def test_begin(self):
        with environment(parent=self.env) as env:
            with READ("""
                (begin
                    (+ a b)
                    (- a b)
                    (* a b))
             """) as sexp:
                assert lisp_eval(sexp, env) == 6

class TestCond(unittest.TestCase):
    def setUp(self):
        self.env = Frame.global_frame()
        self.env.setf("a", 2)
        self.env.setf("b", 3)

    def test_begin(self):
        with environment(parent=self.env) as env:
            with READ("""
                (cond
                    ((= a b) 0)
                    ((< a b) 1)
                    ((> a b) 1 2 3 4))
             """) as sexp:
                assert lisp_eval(sexp, env) == 1
            with READ("""
                (cond
                    ((= a b) 0)
                    ((> a b) 1)
                    ((< a b) 1 2 3 4))
             """) as sexp:
                assert lisp_eval(sexp, env) == 4
            with READ("""
                (cond
                    ((= a b) 0)
                    ((> a b) 1)
                    (else 3))
             """) as sexp:
                assert lisp_eval(sexp, env) == 3

class TestAssign(unittest.TestCase):
    def test_set(self):
        with EVAL("""
        (begin
            (set! x 42)
            x
        )
        """, x="7") as result:
            assert result == 42

class TestRecursiveFunction(unittest.TestCase):
    def test_sum(self):
        with EVAL("""
            (+ a b)
        """, a="2", b="(+ 1 1)") as result:
            assert result == 4
    def test_fac(self):
        with EVAL("""
        (begin
            (define fac (lambda (n)
                (cond
                    ((< n 1) 0)
                    ((= n 1) 1)
                    (else (* n (fac (- n 1)))))
            ))
            (fac 5)
        )
        """) as result:
            assert result == 120

class TestProcDefine(unittest.TestCase):
    def test_proc(self):
        """SICP page 12"""
        with EVAL("""
        (begin
            (define (square x) (* x x))
            (square 5)
        )
        """) as result:
            assert result == 25


# vim: set ft=python ts=4 sw=4 expandtab :

