(define (fac n)
  (cond ((= n 1) 1)
        ((> n 1) (* n (fac (- n 1))))))

(fac 5)
