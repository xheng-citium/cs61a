; Some utility functions that you may find useful.
;
; Apply proc to all items
(define (apply-to-all proc items)
  (if (null? items)
      '()
      (cons (proc (car items))
            (apply-to-all proc (cdr items)))))

; Keep those items of a sequence if satisfy the predicate 
(define (keep-if predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (keep-if predicate (cdr sequence))))
        (else (keep-if predicate (cdr sequence)))))

; 
; 
; op: a combiner function taking 2 arguments
(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cddr x) (cdr (cdr x)))
(define (cadar x) (car (cdr (car x))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Problem 18
;; Turns a list of pairs into a pair of lists
(define (zip pairs)
  ; YOUR-CODE-HERE
  (define fronts (apply-to-all car pairs))
  (define tails  (apply-to-all cadr pairs))
  (list fronts tails)
 ) 
; expect zip

(display "Testing Problem 18 ")
(zip '()) 
; expect (() ())
(zip '((1 2))) 
; expect ((1) (2))
(zip '((1 2) (3 4) (5 6))) 
; expect ((1 3 5) (2 4 6))

(zip '((1 . 2)))
; expect Error

(zip '(1))
; expect Error


; Problem 19
;; A list of all ways to partition TOTAL, where each partition must
;; be at most MAX-VALUE and there are at most MAX-PIECES partitions. 

(define (list-partitions total max-pieces max-value)
 ; 'YOUR-CODE-HERE
 ; Step 1: Find all partitions with total and max-value; Ignore max-pieces
 (define (partitions-no-max-pieces total max-value result)
  (cond ((= total 0) (list result)) 
        ((or (< max-value 1) (< total 0)) nil)
        (else (append (partitions-no-max-pieces (- total max-value) max-value (append result (list max-value)))
                      (partitions-no-max-pieces total (- max-value 1) result) )
        )))
 (define result-no-max-pieces (partitions-no-max-pieces total max-value nil))

 ; Step 2: Keep-if the lists that satisfy the max-pieces condition
 (keep-if (lambda (x) (<= (length x) max-pieces)) result-no-max-pieces)
)

(display "Testing Problem 19 ")
(list-partitions 5 2 4) 
; expect ((4 1) (3 2))

(list-partitions 7 3 5) 
; expect ((5 2) (5 1 1) (4 3) (4 2 1) (3 3 1) (3 2 2))

(list-partitions 5 4 3) 
; expect ((3 2) (3 1 1) (2 2 1) (2 1 1 1))
(list-partitions 7 2 4) 
; expect ((4 3))

(list-partitions 7 7 1) 
; expect ((1 1 1 1 1 1 1))

(list-partitions 7 6 1) 
; expect ()


; Problem 20
;; Returns a function that takes in an expression and checks if it is the special
;; form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (analyze expr)
  (cond ((atom? expr)
         ;'YOUR-CODE-HERE
         expr
         )
        ((quoted? expr)
         ;'YOUR-CODE-HERE
         expr          
         )
        ((or (lambda? expr)
             (define? expr))
         ; example '(lambda (let a b) (+ let a b)))
         ; example '(lambda (x) a (let ((a x)) a)))
            (let ((form   (car expr))  ;      lambda           lambda 
                  (params (cadr expr)) ;    (let a b)             (x)
                  (body   (cddr expr))) ; (+ let a b)  (a (let ((a x)) a)) 
              ;'YOUR-CODE-HERE
              (define new-body (apply-to-all analyze body))
              (define new-formals (apply-to-all analyze params))
              (append (list form new-formals) new-body)
            ))
        ((let? expr)
         ; example '(let ((a 1) (b 2)) (+ a b)))
            (let ( (values (cadr expr)) ; ((a 1) (b 2))
                   (body   (apply-to-all analyze (cddr expr)))); ((+ a b))
                 ;'YOUR-CODE-HERE
                 (define zipped (zip values))
                 (define args (car zipped))
                 (define args-values (apply-to-all analyze (cadr zipped)))
                 (cons (append (list 'lambda args) body) args-values) 
            ))
        (else
         ;'YOUR-CODE-HERE
         (apply-to-all analyze expr)); expr is a list
    )
)


;; Problem 20
(analyze)
; expect Error

; Test atomic expr and quoted expr 
(analyze 1) 
; expect 1
(analyze '1)
; expect 1
(analyze 'nil)
; expect ()
(analyze nil)
; expect ()
(analyze 'a) 
; expect a
(analyze '(+ 1 2)) 
; expect (+ 1 2)

; quoted expr remains the same
(analyze '(quote (let ((a 1) (b 2)) (+ a b)))) 
; expect (quote (let ((a 1) (b 2)) (+ a b)))

; Test let expression
(analyze '(let ((a 1) (b 2)) (+ a b))) 
; expect ((lambda (a b) (+ a b)) 1 2)
(analyze '(let ((a (let ((a 2)) a)) (b 2))
            (+ a b))) 
; expect ((lambda (a b) (+ a b)) ((lambda (a) a) 2) 2)
(analyze '(let ((a 1))  (let ((b a)) b) ) ) 
; expect ((lambda (a) ((lambda (b) b) a)) 1)

; let form appears in the body of lambda form
(analyze '(lambda (x) a (let ((a x)) a)))
; expect (lambda (x) a ((lambda (a) a) x))

; let form appears in the formals of the lambda form
(analyze '(lambda (x (let ((y 1)) y)) (+ x y)))
; expect (lambda (x ((lambda (y) y) 1)) (+ x y))


;; Problem 21 (optional)
;; Draw the hax image using turtle graphics.
(define (hax d k)
  'YOUR-CODE-HERE
  nil)


