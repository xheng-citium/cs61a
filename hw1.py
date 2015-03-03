#!/usr/bin/python3

from operator import add, sub

def a_plus_abs_b(a, b):
    # Return a+abs(b), but without calling abs.
    if b < 0:
        f = sub
    else:
        f = add
    return f(a,b)

def two_of_three(a, b, c):
    """Return x*x + y*y, where x and y are the two largest members of the
    positive numbers a, b, and c.

    >>> two_of_three(1, 2, 3)
    13
    >>> two_of_three(5, 3, 1)
    34
    >>> two_of_three(10, 2, 8)
    164
    >>> two_of_three(5, 5, 5)
    50
    """
    return a*a + b*b + c*c - min(a,b,c) **2

#############################################################
# with_if_statement() returns the number 1, but with_if_function() does not (it can do anything else):
def if_function(condition, true_result, false_result):
    """Return true_result if condition is a true value, and
    false_result otherwise.

    >>> if_function(True, 2, 3)
    2
    >>> if_function(False, 2, 3)
    3
    >>> if_function(3==2, 3+2, 3-2)
    1
    >>> if_function(3>2, 3+2, 3-2)
    5
    """
    if condition:
        return true_result
    else:
        return false_result

def with_if_statement():
    """
    >>> with_if_statement()
    1
    """
    if c():
        return t()
    else:
        return f()

def with_if_function():
    return if_function(c(), t(), f())

def c():
    if "x" not in globals():
        global x
        x = 1
    return True if x == 1 else False

def t():
    return 1 if x == 1 else 0

def f():
    global x 
    x = 2
    return 1 if x == 1 else 0

###################################################################
def hailstone(n):
    """Print the hailstone sequence starting at n and return its
    length.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    steps = 0
    while n > 1:
        print(n)
        steps += 1
        if n % 2 == 1:
            n = n*3+1
        else:
            n = n//2
    print(n)
    steps += 1
    return steps
        
if __name__ == "__main__":
    # Q1
    print("\nQ1")
    print(a_plus_abs_b(2, 3))
    print(a_plus_abs_b(2, -3))
    
    #Q2
    print("\nQ2")
    print(two_of_three(1, 2, 3))
    print(two_of_three(5, 3, 1))
    print(two_of_three(10, 2, 8))
    print(two_of_three(5, 5, 5))

    #Q3
    print("\nQ3")
    print(with_if_statement())
    print(with_if_function())
   
    #Q4
    print("\nQ4:Hailstone")
    a = hailstone(10)
    print("hailstone(10) steps =", a)
    a = hailstone(1)
    print("hailstone(1) steps =", a)

    #TODO: Challenge question



