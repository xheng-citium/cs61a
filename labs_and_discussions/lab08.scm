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

(define (cube x)
  ;'your-code-here
  (* x x x)
)

; Tests for cube
(if (not (equal? (cube 0) 
          ;'your-code-here
          ))
    (begin
      (assert-equal 1 "cube" (cube 2) 8)
      (assert-equal 2 "cube" (cube 3) 27)
      (assert-equal 3 "cube" (cube 1) 1)
      (assert-equal 4 "cube" (cube 45) 91125))
    (display "cube not implemented!"))

(define (over-or-under x y)
  ;'your-code-here
  (if (> x y) 
   'over
   (if (= x y) 
    'equals 
    'under)))

; Tests for over-or-under
(if (not (equal? (over-or-under 0 0) 'your-code-here))
    (begin
      (assert-equal 1 "over-or-under" (over-or-under 5 5) 'equals)
      (assert-equal 2 "over-or-under" (over-or-under 5 4) 'over)
      (assert-equal 3 "over-or-under" (over-or-under 3 5) 'under))
    (display "over-or-under not implemented!"))

(define (make-adder num)
  'your-code-here
)

; Tests for make-adder
(define add-two (make-adder 2))
(define add-three (make-adder 3))
(if (not (equal? (make-adder 1) 'your-code-here))
    (begin
      (assert-equal 1 "make-adder" (add-two 2) 4)
      (assert-equal 2 "make-adder" (add-two 3) 5)
      (assert-equal 3 "make-adder" (add-three 3) 6)
      (assert-equal 4 "make-adder" (add-three 9) 12))
    (display "make-adder not implemented!"))

(define (composed f g)
  'your-code-here
)

; Tests for composed
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

(define structure
  'your-code-here
)

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

