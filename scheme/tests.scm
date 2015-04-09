;;; Test cases for Scheme.
;;;
;;; In order to run only a prefix of these examples, add the line
;;;
;;; (exit)
;;;
;;; after the last test you wish to run.

;;; **********************************
;;; *** Add more of your own here! ***
;;; **********************************

; Added by xin heng

; Problem 1 and 2
'foo 
; expect foo

(1 . )
; expect Error: unexpected token: ) 

)
; expect Error: unexpected token: )

(1 2))
; expect Error: unexpected token: ) 

(2)
; expect Error

'(1 . 4) 
; expect (1 . 4)

'(1 (2 three . (4 . 5))) 
; expect (1 (2 three 4 . 5))

; Problem 3 and 4
; NB This is a bug in scheme_oddp. Should not allow floating number in my opinion
(odd? 0.1) 
; expect False

(odd? 3.0)
; expect True

(odd? 3)
; expect True

+ 
; expect #[primitive]

(+ 1 3 

  10  ) ; spaces and newlines are ok
; expect 14

(+1 3)
; expect Error: Cannot call 1

(* 1 3 

  10  )
; expect 30

(/ 1 3 
  10) ; div must be between two numbers
; expect Error

(/ 1 3) 
; expect 0.3333333333333333

(/ 1 4)
; expect 0.25

(/ 1 0)
; expect Error: division by zero

(eval 1)
; expect 1

(eval)
; expect Error: Failed call of the function: <function scheme_eval at 0x7f9d93906268>

(boolean? #t)
; expect True

(boolean? 0)
; expect False

(boolean? 'c)
; expect False

(not #f)
; expect True

(not 0)
; expect False

(eq? 1 1.0)
; expect True

(pair? (cons 1 2) )
; expect True

(null? nil)
; expect True

(list? (cons 1  2) )
; expect False

(list? '(1  2) )
; expect True

(atom? #t)
; expect True

(atom? 1.0)
; expect True

(atom? 'hello)
; expect True

(atom? nil)
; expect True

(atom? '(1 2))
; expect False


; Problem 5A, do_define_form, 1st part
(define tau ( * 2 3.1415926)) 
; expect tau

tau 
; expect 6.2831852

'tau
; expect tau

tauu
; expect Error

(define tau 'x)
; return tau

(define 3c 3)
; expect 3c

(define #c 3)
; expect Error: too few operands in for


; Problem 6B
(quote x)
; expect x

(quote (a b))
;expect (a b)

(car (quote (a b))) 
; expect a

(eval (cons 'car '('(1 2)))) 
; expect 1

'(1 2 . 3)
; expect (1 2 . 3)

'(cs . student) ; form a dotted list
; expect (cs . student)

'(cs student) ; form a scheme list
; expect (cs student)

'(cs . (student)) ; same as above; a more complex way of forming a list
; expect (cs student)


'(hi there . (cs . (student)))
; expect (hi there cs student)


'()
; expect ()

')
; expect Error: unexpected token: )

(quote x 1)
; expect Error: too many operands in form

(quote)
; expect Error: too few operands in form


; Problem 7
(begin)
; expect Error

(begin (+ 2 3) (+ 5 6)) 
; expect 11

(begin (begin 2 4))
; expect 4

(begin (begin 2 4) 5)
; expect 5

(begin (begin 2 4) (begin 5) )
; expect 5

(define x (begin (newline) (+ 2 3))) 
; expect x
(+ x 3) 
; expect 8


(begin '(+ 2 3)) 
; expect (+ 2 3)

(eval (begin '(+ 2 3)) )
; expect 5

(begin 30 'hello) 
; expect hello

(begin 30 hello)
; expect Error: unknown identifier hello

(begin (print 'hello) '(+ 4 3))
; expect hello ; (+ 4 3)

(begin (define x 1) (define x (begin (define y 2))) x)
; expect y


; Problem 8
(lambda (x) )
; expect Error: too few operands in form 

(lambda (x) 2 (+ x 2))
; expect (lambda (x) (begin 2 (+ x 2)))

(lambda (x y) (+ x y)) 
; expect (lambda (x y) (+ x y))

(lambda (x) (+ x y) ) 
; expect (lambda (x) (+ x y))

(lambda (y) (print y) (* y 2)) 
; expect (lambda (y) (begin (print y) (* y 2)))

(define f (lambda (x) (* x 2))) 
; expect f
(f 20)
; expect 40


; Problem 9A

(define x)
; expect Error
(define #f 2)
; expect Error

(define x 'xx)
; expect x
(eval x)
; expect Error
(define xx 10)
; expect xx
(eval x)
; expect 10

(define (f x))
; expect Error

(define (f ) 4) ; anonymous function
; expect f
(f)
; expect 4

(define (f x) (+ x 2)) 
; expect f
(f 10)
; expect 12
(f #t) ; #t is considered as 1 in arithmetic calc
; expect 3
(eq? #t 1) ; eq? operator discloses #t and #f 's numerical representation
; expect True
(eq? #f 0)
; expect True
(eq? #t 2)
; expect False

(define (square x) (* x x)) 
; expect square
square 
; expect (lambda (x) (* x x))

(define (pos x y) (and (>= x 0) (>= y 0)))
; expect pos
pos
; expect (lambda (x y) (and (>= x 0) (>= y 0)))
(pos 1 -1)
; expect False
(pos #t 1)
; expect True


; Problem 10, 11B and 12
(begin (define v 2) (define v #f) v) ; repeats is fine in make_call_frame
; expect False

(let (v 2) (v #f) v) ; repeats is not fine. But it is not make_call_frame's job. It is do_let_form's job
; expect Error

(lambda (x y) 1) ; check_formals should not error out
; expect (lambda (x y) 1)
(lambda (x 'hello) (+ x 1))
; expect Error: (quote hello) is not a valid symbol 
(begin #t (define #f #f))
; expect Error

(lambda (x 10) (+ x 1))
; expect Error

(lambda (x y x) 1) 
; expect Error: x appears more than once

(lambda (x y) (/ x y) ) 
; expect (lambda (x y) (/ x y))


; Problem 13A
(if (= 4 2) #t #f) 
; expect False

(if + 1) ; operators mean True
; expect 1
(if = 1)
; expect 1


(if 0 1 0)
; expect 1
(if 1 1 0)
; expect 1
(if 'hello 1 0)
; expect 1
(if (cons 1 2) 1 0)
; expect 1
(if (car (cons #f #t)) 1 0)
; expect 0

(if #t '(1 2))
; expect (1 2)
(if #t '(1 . 2))
; expect (1 . 2)

(if (= 4 4) (* 1 2) (+ 3 4)) 
; expect 2

(if (= 4 2) #t) 
; expect okay

(if () 1) ; nil means True
; expect 1

(if (if ( = 4 2) 1 0) 1)
; expect 1

(if (if ( = 4 2) 1 #f) 1)
; expect okay


; Problem 14B
(and)
; expect True

(and #f ())
; expect False
(and ()) ; nil means True
; expect ()
(and () 2) ; 
; expect 2


(and (and #t 1) #t)
; expect True

(and #t #t (= 4 5)) ; these 3 examples show returning the last value regardless its true or false 
; expect False
(and #t 0 5)
; expect 5
(and #t 0 'hello)
; expect hello

(and #t #f 42 (/ 1 0)) ; early exit
; expect False

(and 4 5 6)  
; expect 6

(or) 
; expect False

(or '(1))
; expect (1)

(or (1 . 2))
; expect Error: malformed list

(or (1) )
; expect Error

(or ())
; expect ()

(or nil #f)
; expect ()

(or (or))
; expect False

(or (and #t 1) #t)
; expect 1

(or 5 2 1)  
; expect 5

(or 4 #t (/ 1 0)) 
; expect 4

(or #f #f (> 2 3)) 
; expect False

(or 0 #t #f) ; NB this small example shows inconsistency of the relationship between 0 and #f
; expect 0
(eq? #f 0)
; expect True


(or 'a #f) 
; expect a
(or '3c #f #f)
; expect 3c

(or (< 2 3) (> 2 3) 2 x) ; doesn't matter if x is not defined
; expect True

(or #f (> 2 3) (= 2 2)) 
; expect True


; Problem 15A
(cond)
; expect okay
(cond (1 2))
; expect 2

(cond (#f bad-expr) 
      ((+ 1 2))
 )
; expect 3

(cond ((= 4 3) 'nope)
      ((= 4 4) 'hi)
      (else 'wait)) 
; expect hi

(cond ((= 4 3) 'wat)
      ((= 4 4)) ; body of cond case is empty
      (else 'hm)) 
; expect True

(cond ((= 4 4) 'here 42)
      (else 'wat 0)) 
; expect 42

(cond (else 0 'wat)) 
; expect wat

(cond (else)) ; NB it is #t in STk
; expect Error: badly formed else clause 

(cond (else 'wat)
      ((= 4 4) 'here 42)
      ) 
; expect Error: else must be last

(cond ((= 4 3) 'here 42)
      (else ()) ) 
; expect ()

(cond ((= 4 3) 'here 42)
      (else ) ) 
; expect Error: badly formed else clause

(cond ((= 4 4) 'here 42)
      (else ) ) ; early exist so bad else clause is ok 
; expect 42

(cond (12)) 
; expect 12

(cond ((= 4 3))
      ('hi)) ; returns predicate quoted 
; expect hi

(cond ((= 4 3))
      (#f)) ; predicate is false
; expect okay

(cond (#f 1)) 
; expect okay

(cond ((> 2 3) 4 5)
      ((> 2 4) 5 6)
      ((< 2 5) 6 7)
      (else 7 8)) 
; expect 7

(cond ((> 2 3) (display 'oops) (newline))
      (else 9)) 
; expect 9


; Problem 16
(let () 2)
; expect 2

(let ((x 3.0)) (* x x))
; expect 9

(let ((let ((x 3.0)) (* x x) )) 2) ; cannot have a let inside let; same as STk
; expect Error: too many operands in form

(let ((define f 2)) 2) ; cannot have define inside let; same as STk
; expect Error 
(let ( (f (lambda (y) 2))) (eq? 2 (f 10)) ) ; sln: use lambda to replace define
; expect True
(print f)
; expect okay

(let)
; expect Error: too few operands in form 

(let ((x 2)) (let () 3))
; expect 3


(let ((v 2) (v 3) v))
; expect Error: v appears more than once

(let ((x 2)) )
; expect Error: too few operands in form
(let (x 2) x) 
; expect Error: badly formed expression: x

(let ((a 1 1)) a)
; Error: too many operands in form

(let ((a 1) (b)) a)
; expect Error: too few operands in form

(let ((a 1) (2 2)) a)
; expect Error: 2 is not a valid symbol

(let ((a 1) (b 2)) c)
; expect Error: unknown identifier: c 


(define x 'hi) 
; expect x
(define y 'bye) 
; expect y
(let ((x 42) (y (* 5 10)))
     (list x y)) 
; expect (42 50)
(list x y) 
; expect (hi bye)

(let ((x 42)) x 1 2) 
; expect 2

(let ((x 5))
     (let ((x 2)
          (y x))
          (+ y (* x 2))) ; y = 5
     ) 
; expect 9

(let ((x 2) (y 3))
 (* x y)) 
; expect 6

(let ((x 1)
      (y 3))
      (define x (+ x 1))
      (cons x y) ) ; Pair(2, 3)
; expect (2 . 3)

(let ((x 2) (y 3))
 (let ((x 6)
       (foo (lambda (z) (+ x y z)))
      )
  (foo 4) ) ) ; expect 9, b/c x is 2
; expect 9

(let ((a 200))
 (let ((a 1) (b a)) 
  b)) ; expect 200, and the next case should fail
; expect 200

(let ((a 1) (b a)) b) 
; Error: unknown identifier: a


; Problem 17
(define f (mu (x) (+ x y))) 
; expect f
(define g (lambda (x y) (f (+ x x)))) 
; expect g
(g 3 7) 
; expect 13

(define add (mu () (+ x y)))
; expect add
(define (f x y) (add) )
; expect f
(f 10 25)
; expect 35


(define (f x y) add )
; expect f
(f 10 25)
; expect (mu () (+ x y))

; nested mu expr
(define f (mu () (+ x y)))
(define g (mu (x y) (f)))
(g 2 3)
; expect 5


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;; These are examples from several sections of "The Structure
;;; and Interpretation of Computer Programs" by Abelson and Sussman.

;;; License: Creative Commons share alike with attribution

;;; 1.1.1

10
; expect 10

(+ 137 349)
; expect 486

(- 1000 334)
; expect 666

(* 5 99)
; expect 495

(/ 10 5)
; expect 2

(+ 2.7 10)
; expect 12.7

(+ 21 35 12 7)
; expect 75

(* 25 4 12)
; expect 1200

(+ (* 3 5) (- 10 6))
; expect 19

(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))
; expect 57

(+ (* 3
      (+ (* 2 4)
         (+ 3 5)))
   (+ (- 10 7)
      6))
; expect 57

;;; 1.1.2

(define size 2)
; expect size
size
; expect 2

(* 5 size)
; expect 10

(define pi 3.14159)
(define radius 10)
(* pi (* radius radius))
; expect 314.159

(define circumference (* 2 pi radius))
circumference
; expect 62.8318

;;; 1.1.4

(define (square x) (* x x))
; expect square
(square 21)
; expect 441

(define square (lambda (x) (* x x))) ; See Section 1.3.2
(square 21)
; expect 441

(square (+ 2 5))
; expect 49

(square (square 3))
; expect 81

(define (sum-of-squares x y)
  (+ (square x) (square y)))
(sum-of-squares 3 4)
; expect 25

(define (f a)
  (sum-of-squares (+ a 1) (* a 2)))
(f 5)
; expect 136

;;; 1.1.6

(define (abs x)
  (cond ((> x 0) x)
        ((= x 0) 0)
        ((< x 0) (- x))))
(abs -3)
; expect 3

(abs 0)
; expect 0

(abs 3)
; expect 3

(define (a-plus-abs-b a b)
  ((if (> b 0) + -) a b))
(a-plus-abs-b 3 -2)
; expect 5


;;; 1.1.7

(define (sqrt-iter guess x)
  (if (good-enough? guess x)
      guess
      (sqrt-iter (improve guess x)
                 x)))
(define (improve guess x)
  (average guess (/ x guess)))
(define (average x y)
  (/ (+ x y) 2))
(define (good-enough? guess x)
  (< (abs (- (square guess) x)) 0.001))
(define (sqrt x)
  (sqrt-iter 1.0 x))
(sqrt 9)
; expect 3.00009155413138

(sqrt (+ 100 37))
; expect 11.704699917758145

(sqrt (+ (sqrt 2) (sqrt 3)))
; expect 1.7739279023207892

(square (sqrt 1000))
; expect 1000.000369924366

;;; 1.1.8

(define (sqrt x)
  (define (good-enough? guess)
    (< (abs (- (square guess) x)) 0.001))
  (define (improve guess)
    (average guess (/ x guess)))
  (define (sqrt-iter guess)
    (if (good-enough? guess)
        guess
        (sqrt-iter (improve guess))))
  (sqrt-iter 1.0))
(sqrt 9)
; expect 3.00009155413138

(sqrt (+ 100 37))
; expect 11.704699917758145

(sqrt (+ (sqrt 2) (sqrt 3)))
; expect 1.7739279023207892

(square (sqrt 1000))
; expect 1000.000369924366

;;; 1.3.1


(define (cube x) (* x x x))
(define (sum term a next b)
  (if (> a b)
      0
      (+ (term a)
         (sum term (next a) next b))))
(define (inc n) (+ n 1))
(define (sum-cubes a b)
  (sum cube a inc b))
(sum-cubes 1 10)
; expect 3025

(define (identity x) x)
(define (sum-integers a b)
  (sum identity a inc b))
(sum-integers 1 10)
; expect 55

;;; 1.3.2

((lambda (x y z) (+ x y (square z))) 1 2 3)
; expect 12

(define (f x y)
  (let ((a (+ 1 (* x y)))
        (b (- 1 y)))
    (+ (* x (square a))
       (* y b)
       (* a b))))
(f 3 4)
; expect 456

(define x 5)
(+ (let ((x 3))
     (+ x (* x 10)))
   x)
; expect 38

(let ((x 3)
      (y (+ x 2)))
  (* x y))
; expect 21

;;; 2.1.1

(define (add-rat x y)
  (make-rat (+ (* (numer x) (denom y))
               (* (numer y) (denom x)))
            (* (denom x) (denom y))))
(define (sub-rat x y)
  (make-rat (- (* (numer x) (denom y))
               (* (numer y) (denom x)))
            (* (denom x) (denom y))))
(define (mul-rat x y)
  (make-rat (* (numer x) (numer y))
            (* (denom x) (denom y))))
(define (div-rat x y)
  (make-rat (* (numer x) (denom y))
            (* (denom x) (numer y))))
(define (equal-rat? x y)
  (= (* (numer x) (denom y))
     (* (numer y) (denom x))))

(define x (cons 1 2))
(car x)
; expect 1

(cdr x)
; expect 2

(define x (cons 1 2))
(define y (cons 3 4))
(define z (cons x y))
(car (car z))
; expect 1

(car (cdr z))
; expect 3

z
; expect ((1 . 2) 3 . 4)

(define (make-rat n d) (cons n d))
(define (numer x) (car x))
(define (denom x) (cdr x))
(define (print-rat x)
  (display (numer x))
  (display '/)
  (display (denom x))
  (newline))
(define one-half (make-rat 1 2))
(print-rat one-half)
; expect 1/2 ; okay

(define one-third (make-rat 1 3))
(print-rat (add-rat one-half one-third))
; expect 5/6 ; okay

(print-rat (mul-rat one-half one-third))
; expect 1/6 ; okay

(print-rat (add-rat one-third one-third))
; expect 6/9 ; okay

(define (gcd a b)
  (if (= b 0)
      a
      (gcd b (remainder a b))))
(define (make-rat n d)
  (let ((g (gcd n d)))
    (cons (/ n g) (/ d g))))
(print-rat (add-rat one-third one-third))
; expect 2/3 ; okay

(define one-through-four (list 1 2 3 4))
one-through-four
; expect (1 2 3 4)

(car one-through-four)
; expect 1

(cdr one-through-four)
; expect (2 3 4)

(car (cdr one-through-four))
; expect 2

(cons 10 one-through-four)
; expect (10 1 2 3 4)

(cons 5 one-through-four)
; expect (5 1 2 3 4)

(define (map proc items)
  (if (null? items)
      nil
      (cons (proc (car items))
            (map proc (cdr items)))))
(map abs (list -10 2.5 -11.6 17))
; expect (10 2.5 11.6 17)

(map (lambda (x) (* x x))
     (list 1 2 3 4))
; expect (1 4 9 16)

(define (scale-list items factor)
  (map (lambda (x) (* x factor))
       items))
(scale-list (list 1 2 3 4 5) 10)
; expect (10 20 30 40 50)

(define (count-leaves x)
  (cond ((null? x) 0)
        ((not (pair? x)) 1)
        (else (+ (count-leaves (car x))
                 (count-leaves (cdr x))))))
(define x (cons (list 1 2) (list 3 4)))
(count-leaves x)
; expect 4

(count-leaves (list x x))
; expect 8

;;; 2.2.3

(define (odd? x) (= 1 (remainder x 2)))
(define (filter predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (filter predicate (cdr sequence))))
        (else (filter predicate (cdr sequence)))))
(filter odd? (list 1 2 3 4 5))
; expect (1 3 5)

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))
(accumulate + 0 (list 1 2 3 4 5))
; expect 15

(accumulate * 1 (list 1 2 3 4 5))
; expect 120

(accumulate cons nil (list 1 2 3 4 5))
; expect (1 2 3 4 5)

(define (enumerate-interval low high)
  (if (> low high)
      nil
      (cons low (enumerate-interval (+ low 1) high))))
(enumerate-interval 2 7)
; expect (2 3 4 5 6 7)

(define (enumerate-tree tree)
  (cond ((null? tree) nil)
        ((not (pair? tree)) (list tree))
        (else (append (enumerate-tree (car tree))
                      (enumerate-tree (cdr tree))))))
(enumerate-tree (list 1 (list 2 (list 3 4)) 5))
; expect (1 2 3 4 5)

;;; 2.3.1

(define a 1)

(define b 2)

(list a b)
; expect (1 2)

(list 'a 'b)
; expect (a b)

(list 'a b)
; expect (a 2)

(car '(a b c))
; expect a

(cdr '(a b c))
; expect (b c)

(define (memq item x)
  (cond ((null? x) false)
        ((eq? item (car x)) x)
        (else (memq item (cdr x)))))
(memq 'apple '(pear banana prune))
; expect False

(memq 'apple '(x (apple sauce) y apple pear))
; expect (apple pear)

(define (equal? x y)
  (cond ((pair? x) (and (pair? y)
                        (equal? (car x) (car y))
                        (equal? (cdr x) (cdr y))))
        ((null? x) (null? y))
        (else (eq? x y))))
(equal? '(1 2 (three)) '(1 2 (three)))
; expect True

(equal? '(1 2 (three)) '(1 2 three))
; expect False

(equal? '(1 2 three) '(1 2 (three)))
; expect False

;;; Peter Norvig tests (http://norvig.com/lispy2.html)

(define double (lambda (x) (* 2 x)))
(double 5)
; expect 10

(define compose (lambda (f g) (lambda (x) (f (g x)))))
((compose list double) 5)
; expect (10)

(define apply-twice (lambda (f) (compose f f)))
((apply-twice double) 5)
; expect 20

((apply-twice (apply-twice double)) 5)
; expect 80

(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))
(fact 3)
; expect 6

(fact 50)
; expect 30414093201713378043612608166064768844377641568960512000000000000

(define (combine f)
  (lambda (x y)
    (if (null? x) nil
      (f (list (car x) (car y))
         ((combine f) (cdr x) (cdr y))))))
(define zip (combine cons))
(zip (list 1 2 3 4) (list 5 6 7 8))
; expect ((1 5) (2 6) (3 7) (4 8))

(define riff-shuffle (lambda (deck) (begin
    (define take (lambda (n seq) (if (<= n 0) (quote ()) (cons (car seq) (take (- n 1) (cdr seq))))))
    (define drop (lambda (n seq) (if (<= n 0) seq (drop (- n 1) (cdr seq)))))
    (define mid (lambda (seq) (/ (length seq) 2)))
    ((combine append) (take (mid deck) deck) (drop (mid deck) deck)))))
(riff-shuffle (list 1 2 3 4 5 6 7 8))
; expect (1 5 2 6 3 7 4 8)

((apply-twice riff-shuffle) (list 1 2 3 4 5 6 7 8))
; expect (1 3 5 7 2 4 6 8)

(riff-shuffle (riff-shuffle (riff-shuffle (list 1 2 3 4 5 6 7 8))))
; expect (1 2 3 4 5 6 7 8)

;;; Additional tests

(apply square '(2))
; expect 4

(apply + '(1 2 3 4))
; expect 10

(apply (if false + append) '((1 2) (3 4)))
; expect (1 2 3 4)

(if 0 1 2)
; expect 1

(if '() 1 2)
; expect 1

(or false true)
; expect True

(or)
; expect False

(and)
; expect True

(or 1 2 3)
; expect 1

(and 1 2 3)
; expect 3

(and False (/ 1 0))
; expect False

(and True (/ 1 0)) ; expect Error

(or 3 (/ 1 0))
; expect 3

(or False (/ 1 0)) ; expect Error

(or (quote hello) (quote world))
; expect hello

(if nil 1 2)
; expect 1

(if 0 1 2)
; expect 1

(if (or false False #f) 1 2)
; expect 2

(define (loop) (loop))
(cond (false (loop))
      (12))
; expect 12

((lambda (x) (display x) (newline) x) 2)
; expect 2 ; 2

(define g (mu () x))
(define (high f x)
  (f))

(high g 2)
; expect 2

(define (print-and-square x)
  (print x)
  (square x))
(print-and-square 12)
; expect 12 ; 144

(/ 1 0) ; expect Error

(define addx (mu (x) (+ x y)))
(define add2xy (lambda (x y) (addx (+ x x))))
(add2xy 3 7)
; expect 13


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Scheme Implementations ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; len outputs the length of list s
(define (len s)
  (if (eq? s '())
    0
    (+ 1 (len (cdr s)))))
(len '(1 2 3 4))
; expect 4


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Move the following (exit) line to run additional tests. ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(exit)



;;;;;;;;;;;;;;;;;;;;
;;; Extra credit ;;;
;;;;;;;;;;;;;;;;;;;;

(exit)

; Tail call optimization test
(define (sum n total)
  (if (zero? n) total
    (sum (- n 1) (+ n total))))
(sum 1001 0)
; expect 501501
