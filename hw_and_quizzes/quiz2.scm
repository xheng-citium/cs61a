; CS 61A Fall 2014
; Name:
; Login:

(define (assert-equal value expression)
  (if (equal? value (eval expression))
    (print 'ok)
    (print (list 'for expression ':
                 'expected value
                 'but 'got (eval expression)))))

; Utility functions
(define (add-two x) (+ x 2))
(define (square x) (* x x))
(define (cadr s) (car (cdr s)))

(define (equal-answer f1 f2)
  'YOUR-CODE-HERE  (lambda (x) 'replace-this))

(define (test-equal-answer)
  (print (list 'testing 'equal-answer))
  ; (add-two 2) evaluates to 4, (square 2) also evaluates to 4
  (assert-equal true  '((equal-answer add-two square) 2))
  ; (add-two 3) evaluates to 5, (square 3) instead evaluates to 9
  (assert-equal false '((equal-answer add-two square) 3))

  )

(test-equal-answer)

(define (num-adjacent-matches s)
  'YOUR-CODE-HERE  'replace-this)

(define (test-num-adjacent-matches)
  (print (list 'testing 'num-adjacent-matches))
  ; no pairs
  (assert-equal 0 '(num-adjacent-matches '(1 2 3 4)))
  ; one pair of 1's
  (assert-equal 1 '(num-adjacent-matches '(1 1 2 3)))
  ; one pair of 1's, one pair of 2's
  (assert-equal 2 '(num-adjacent-matches '(1 1 2 2)))
  ; three pairs of 1's
  (assert-equal 3 '(num-adjacent-matches '(1 1 1 1)))

  )

(test-num-adjacent-matches)

(define (tally names)
  'YOUR-CODE-HERE  'replace-this)

(define (test-tally)
  (print (list 'testing 'tally))
  (assert-equal '((obama . 1))
                '(tally '(obama)))
  (assert-equal '((taft . 3))
                '(tally '(taft taft taft)))
  (assert-equal '((jerry . 2) (brown . 1))
                '(tally '(jerry jerry brown)))
  (assert-equal '((jane . 5) (jack . 2) (jill . 1))
                '(tally '(jane jack jane jane jack jill jane jane)))
  (assert-equal '((jane . 5) (jack . 2) (jill . 1))
                '(tally '(jane jack jane jane jill jane jane jack)))

  )

(define (apply-to-all fn s)
  (if (null? s) nil
      (cons (fn (car s))
            (apply-to-all fn (cdr s)))))

(define (keep-if fn s)
  (cond ((null? s) nil)
        ((fn (car s)) (cons (car s)
                            (keep-if fn (cdr s))))
        (else (keep-if fn (cdr s)))))

; Using this helper procedure is optional. You are allowed to delete it.
(define (unique s)
  'YOUR-CODE-HERE  'replace-this)

; Using this helper procedure is optional. You are allowed to delete it.
(define (count name s)
  'YOUR-CODE-HERE  'replace-this)

; Passing these tests is optional. You are allowed to delete them.
(define (test-tally-helpers)
  (print (list 'testing 'unique))
  (assert-equal '(jane)  '(unique '(jane jane jane)))
  (assert-equal '(jane jack jill)  '(unique '(jane jack jane jack jill jane)))
  (assert-equal '(jane jack jill)  '(unique '(jane jack jane jill jane jack)))

  (print (list 'testing 'count))
  (assert-equal 3 '(count 'jane '(jane jane jane)))
  (assert-equal 0 '(count 'jill '(jane jane jane)))
  (assert-equal 2 '(count 'jack '(jane jack jane jack jill jane)))
  )

(test-tally-helpers)
(test-tally)

