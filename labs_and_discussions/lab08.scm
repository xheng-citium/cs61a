; Don't edit! Used for tests!
(define (assert-equal test-num func-name actual-result expected-result)
  (if (not (equal? expected-result actual-result))
      (begin
        (display "Testing case ")
        (display test-num)
        (display (string-append " for " func-name ": Test failed. "))
        (display "Expected: ")
        (display expected-result)
        (display " Got: ")
        (display actual-result)
        (newline))
      (begin (display "Ok") (newline))))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Question 3
(define (cube x)
 ;'your-code-here
 (* x x x) )

; Tests for cube
(if (not (equal? (cube 0) 
          ;'your-code-here
          0))
 (begin
  (assert-equal 1 "cube" (cube 2) 8)
  (assert-equal 2 "cube" (cube 3) 27)
  (assert-equal 3 "cube" (cube 1) 1)
  (assert-equal 4 "cube" (cube 45) 91125))
 (begin (display "cube not implemented!")
  (newline))
 )

; Tests for cube
(if (equal? (cube 0) 
          ;'your-code-here
          0)
 (begin
  (assert-equal 1 "cube" (cube 2) 8)
  (assert-equal 2 "cube" (cube 3) 27)
  (assert-equal 3 "cube" (cube 1) 1)
  (assert-equal 4 "cube" (cube 45) 91125))
 (display "cube not implemented!")
 )

; Question 4
(define (pos_number x) 
 (if (> x 0) 'positive 
  (if (< x 0) 'negative
   'zero) ) )
(display (pos_number 4))
(newline)
(display (pos_number -4))
(newline)


(define (over-or-under x y)
 ;'your-code-here
 (if (> x y) 'over
  (if (= x y) 'equals 
   'under)))

; Tests for over-or-under
(if (equal? (over-or-under 0 0)  
          ;'your-code-here))
          'equals)
    (begin
      (assert-equal 1 "over-or-under" (over-or-under 5 5) 'equals)
      (assert-equal 2 "over-or-under" (over-or-under 5 4) 'over)
      (assert-equal 3 "over-or-under" (over-or-under 3 5) 'under)
      (newline))
    (begin (display "over-or-under not implemented ")
     (newline) ) )


(define (even_odd x) 
 (cond ((and (> x 0) (= (modulo x 2) 0) ) 'positive-even-integer )
       ((and (> x 0) (= (modulo x 2) 1) ) 'positive-odd-integer )
       ))

(begin (display (even_odd 10))
       (newline)
       (display (even_odd 11)) 
       (newline) )

; Question 5
(define (divisible a b) 
 (cond ((= 0 (modulo a b)) b)
       ((= 0 (modulo b a)) a)
       ((or (<= a 0) (<= b 0)) -1)
       (else 0)
       ))
(display (divisible 10 5))
(newline)
(display (divisible 3 9))
(newline)

(if (= 0 (divisible 2 9)) 
    (display "Divisibility not found") )
(newline)
(if (= -1 (divisible -2 9)) 
    (display "Bad args for divisible() function") )
(newline)

(define (gcd a b)
  (if (> a b)
   (begin (define big a)
          (define small b)) 
   (begin (define big b) 
          (define small a)))
  (if (= small 0) big 
      (begin (define d (divisible big small))
        (if (not (= 0 d)) 
            d
            (gcd b (modulo a b))
            ))))
(begin (newline) (display "Testing gcd() function ") (newline) )

(begin (display (gcd 5 5)) (newline))
(begin (display (gcd 5 10)) (newline))
(begin (display (gcd 10 5)) (newline))
(begin (display (gcd 91 26)) (newline))
(begin (display (gcd 26 91)) (newline))
(begin (display (gcd 27 91)) (newline))

; Tests for gcd
(begin
  (assert-equal 1 "gcd" (gcd 0 4) 4)
  (assert-equal 2 "gcd" (gcd 8 0) 8)
  (assert-equal 3 "gcd" (gcd 34 19) 1)
  (assert-equal 4 "gcd" (gcd 39 91) 13)
  (assert-equal 5 "gcd" (gcd 20 30) 10)
  (assert-equal 6 "gcd" (gcd 40 40) 40))


; Question 6
(newline)(display "Q6, lambda examples") (newline)
(define double (lambda (x) (* 2 x)))
(display (double 10)) (newline)

(define (make-adder num)
  ;'your-code-here
  (lambda (x) (+ x num))
  )

(display "Q6 Tests for make-adder")(newline)
(define add-two (make-adder 2))
(define add-three (make-adder 3))

(if (not (equal? (make-adder 1) 'your-code-here))
    (begin
      (assert-equal 1 "make-adder" (add-two 2) 4)
      (assert-equal 2 "make-adder" (add-two 3) 5)
      (assert-equal 3 "make-adder" (add-three 3) 6)
      (assert-equal 4 "make-adder" (add-three 9) 12))
    (display "make-adder not implemented!"))


; Question 7
(define (composed f g)
  ;'your-code-here
  (lambda (x) (f (g x)))
)


(display "Q7 Tests for composed") (newline)
(define (add-one a) (+ a 1))
(define (multiply-by-two a) (* a 2))
(if (not (equal? (composed + +) 'your-code-here))
    (begin
      ; (+ (+ x 1) 1)
      (assert-equal 1 "composed" ((composed add-one add-one) 2) 4)
      ; (* (* x 2) 2)
      (assert-equal 2 "composed" ((composed multiply-by-two multiply-by-two) 2) 8)
      ; (+ (* x 2) 1)
      (assert-equal 3 "composed" ((composed add-one multiply-by-two) 2) 5)
      ; (* (+ x 1) 2)
      (assert-equal 4 "composed" ((composed multiply-by-two add-one) 2)  6)
      ; (+ (+ (+ x 1) 1) 1)
      (assert-equal 5 "composed" ((composed (composed add-one add-one) add-one) 2) 5)
      ; (+ (+ (* x 2 ) 1) 1)
      (assert-equal 6 "composed" ((composed (composed add-one add-one) multiply-by-two) 2) 6)
      ; (* (+ (+ x 1) 1) 2)
      (assert-equal 7 "composed" ((composed multiply-by-two (composed add-one add-one)) 2) 8))
    (display "composed not implemented!"))

(newline) (display "Lists")(newline)
(define a (cons 1 (cons 2 (cons 3 nil) )))
(display a) (newline)
(display (car a)) (newline)
(display (cdr a)) (newline)
(display (car (cdr (cdr a)))) (newline)

(display (list 1 2 3)) (newline)
(display '(1 2 3)) (newline)
(display '(1 . (2 . (3)))) (newline)

(display "Q8 structure") (newline)
(define structure
  ;'your-code-here
  (cons (list 1) (cons 2 (cons (cons 3 4) (cons 5 nil)) ) ) ; this is correct
)
(display structure) (newline)

(display "Q9: Testing remove() function") (newline)
(define (remove item lst)
 ; 'your-code-here
 (if (null? lst) nil
  (begin (define front (car lst))
         (define tail (cdr lst))
         (cond ((= front item) (remove item tail))
               (else (cons front (remove item tail))))
         )))

(display "(1 2 3) ->") (newline)
(display (remove 1 '(1 2 3))) (newline)
(display (remove 2 '(1 2 3))) (newline)
(display (remove 3 '(1 2 3))) (newline)


(display "Q10: Testing filter() function") (newline)
(define (filter f lst)
 ; 'your-code-here
 (if (null? lst) nil
  (begin (define front (car lst))
         (define tail (cdr lst))
         (cond ((f front) (cons front (filter f tail)))
               (else (filter f tail)))
         )))
(define (positive x) (> x 0) )

(display (filter positive '(-1 2 3))) (newline)
(display (filter positive '(1 -2 3))) (newline)
(display (filter positive '(1 2 -3))) (newline)
(display (filter positive '())) (newline)

(display "Q11: Testing all-satisfies() function") (newline)
(display "     TA has a better solution") (newline)
(define (all-satisfies lst pred)
 ; 'your-code-here
 (if (null? lst) #f
  (begin (define front (car lst))
         (define tail (cdr lst))
         (if (equal? tail nil) (pred front)
             (begin (cond ((pred front) (all-satisfies tail pred))
                          (else #f))))
         )))

(display (all-satisfies '(1 2 3) positive)) (newline)
(display (all-satisfies '(-1 2 3) positive)) (newline)
(display (all-satisfies '(1 -2 3) positive)) (newline)
(display (all-satisfies '(1 2 -3) positive)) (newline)
(display (all-satisfies '() positive)) (newline)

(define (accumulate combiner start n term)
  (if (= n 0)
      start
      'your-code-here
      ))

(define (square x) (* x x))
(define (id x) x)
(define (add-one x) (+ x 1))
(if (not (equal? (accumulate + 0 4 id) 'your-code-here))
    (begin
      ; 0 + 1^2 + 2^2 + 3^2 + 4^2 = 30
      (assert-equal 1 "accumulate" (accumulate + 0 4 square) 30)
      ; 3 * 1 * 2 * 3 * 4 * 5 = 360
      (assert-equal 2 "accumulate" (accumulate * 3 5 id) 360)
      ; 0 + (1 + 1) + (2 + 1) + (3 + 1) = 9
      (assert-equal 3 "accumulate" (accumulate + 0 3 add-one) 9))
    (display "accumulate not implemented!"))

