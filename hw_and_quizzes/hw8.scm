; CS 61A Fall 2014
; Name:
; Login:

(define (assert-equal value expression)
  (if (equal? value (eval expression))
    (print 'ok)
    (print (list 'for expression ':
                 'expected value
                 'but 'got (eval expression)))))

(define (deep-map fn s)
  'YOUR-CODE-HERE  )

(define (square x) (* x x))
(define (double x) (* 2 x))
(define (test-deep-map)
  (assert-equal '(4 9) '(deep-map square '(2 3)))
  (assert-equal '(4 (6 8)) '(deep-map double '(2 (3 4))))
  (assert-equal '(1 4 (9 16 (25 36) ((49)) 64) (81 100))
                '(deep-map square
                '(1 2 (3 4  (5  6)  ((7))  8)  (9  10)))))

(test-deep-map)

(define (substitute s old new)
  'YOUR-CODE-HERE  )

(define (test-substitute)
  (assert-equal '(c a l) '(substitute '(c a b) 'b 'l))
  (assert-equal '((lead axe) (bass axe) (rhythm axe) drums)
                '(substitute '((lead guitar) (bass guitar) (rhythm guitar) drums)
                             'guitar 'axe)))

(test-substitute)

(define (substitute-list s olds news)
  'YOUR-CODE-HERE  )

(define (test-substitute-list)
  (assert-equal '((four calling birds) (three french hens) (two turtle doves))
                '(substitute-list
                  '((4 calling birds) (3 french hens) (2 turtle doves))
                  '(1 2 3 4)
                  '(one two three four))))

(test-substitute-list)

; Derive returns the derivative of exp with respect to var.
(define (derive expr var)
  (cond ((number? expr) 0)
        ((variable? expr) (if (same-variable? expr var) 1 0))
        ((sum? expr) (derive-sum expr var))
        ((product? expr) (derive-product expr var))
        ((exp? expr) (derive-exp expr var))
        (else 'Error)))

; Variables are represented as symbols
(define (variable? x) (symbol? x))
(define (same-variable? v1 v2)
  (and (variable? v1) (variable? v2) (eq? v1 v2)))

; Numbers are compared with =
(define (=number? expr num)
  (and (number? expr) (= expr num)))

; Sums are represented as lists that start with +.
(define (make-sum a1 a2)
  (cond ((=number? a1 0) a2)
        ((=number? a2 0) a1)
        ((and (number? a1) (number? a2)) (+ a1 a2))
        (else (list '+ a1 a2))))
(define (sum? x)
  (and (pair? x) (eq? (car x) '+)))
(define (addend s) (cadr s))
(define (augend s) (caddr s))

; Products are represented as lists that start with *.
(define (make-product m1 m2)
(cond ((or (=number? m1 0) (=number? m2 0)) 0)
      ((=number? m1 1) m2)
      ((=number? m2 1) m1)
      ((and (number? m1) (number? m2)) (* m1 m2))
      (else (list '* m1 m2))))
(define (product? x)
  (and (pair? x) (eq? (car x) '*)))
(define (multiplier p) (cadr p))
(define (multiplicand p) (caddr p))

(define (test-sum)
  (assert-equal '(+ a x)       '(make-sum 'a 'x))
  (assert-equal '(+ a (+ x 1)) '(make-sum 'a (make-sum 'x 1)))
  (assert-equal 'x             '(make-sum 'x 0))
  (assert-equal 'x             '(make-sum 0 'x))
  (assert-equal 4              '(make-sum 1 3)))

(define (test-product)
  (assert-equal '(* a x) '(make-product 'a 'x))
  (assert-equal 0        '(make-product 'x 0))
  (assert-equal 'x       '(make-product 1 'x))
  (assert-equal 6        '(make-product 2 3)))

(test-sum)
(test-product)

(define (derive-sum expr var)
  'YOUR-CODE-HERE  )

(define (test-derive-sum)
  (assert-equal 1 '(derive '(+ x 3) 'x)))

(test-derive-sum)

(define (derive-product expr var)
  'YOUR-CODE-HERE  )

(define (test-derive-product)
  (assert-equal 'y '(derive '(* x y) 'x))
  (assert-equal '(+ (* x y) (* y (+ x 3)))
                '(derive '(* (* x y) (+ x 3)) 'x)))

(test-derive-product)

; Exponentiations are represented as lists that start with ^.
(define (make-exp base exponent)
  'YOUR-CODE-HERE  )

(define (base exp)
  'YOUR-CODE-HERE  )

(define (exponent exp)
  'YOUR-CODE-HERE  )

(define (exp? exp)
  'YOUR-CODE-HERE  )

(define x^2 (make-exp 'x 2))
(define x^3 (make-exp 'x 3))

(define (test-exp)
  (assert-equal 'x '(make-exp 'x 1))
  (assert-equal 1  '(make-exp 'x 0))
  (assert-equal 16 '(make-exp 2 4))
  (assert-equal '(^ x 2) 'x^2)
  (assert-equal 'x    '(base x^2))
  (assert-equal 2     '(exponent x^2))
  (assert-equal true  '(exp? x^2))
  (assert-equal false '(exp? 1))
  (assert-equal false '(exp? 'x))
)

(test-exp)

(define (derive-exp exp var)
  'YOUR-CODE-HERE  )

(define (test-derive-exp)
  (assert-equal '(* 2 x)                   '(derive x^2 'x))
  (assert-equal '(* 3 (^ x 2))             '(derive x^3 'x))
  (assert-equal '(+ (* 3 (^ x 2)) (* 2 x)) '(derive (make-sum x^3 x^2) 'x))
)

(test-derive-exp)

