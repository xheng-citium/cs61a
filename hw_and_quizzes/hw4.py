#!/usr/bin/python3

# CS 61A Fall 2014
# Name: Xin Heng
import pdb

def interval(a, b):
    """Construct an interval from a to b."""
    if a < b:
        return [a, b]
    else: return [b, a]

def lower_bound(x):
    """Return the lower bound of interval x."""
    return x[0]

def upper_bound(x):
    """Return the upper bound of interval x."""
    return x[1]

def str_interval(x):
    """Return a string representation of interval x.
    >>> str_interval(interval(-1, 2))
    '-1 to 2'
    """
    return '{0} to {1}'.format(lower_bound(x), upper_bound(x))

def add_interval(x, y):
    """Return an interval that contains the sum of any value in interval x and
    any value in interval y.
    >>> str_interval(add_interval(interval(-1, 2), interval(4, 8)))
    '3 to 10'
    """
    lower = lower_bound(x) + lower_bound(y)
    upper = upper_bound(x) + upper_bound(y)
    return interval(lower, upper)

def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y.
    >>> str_interval(mul_interval(interval(-1, 2), interval(4, 8)))
    '-8 to 16'
    """
    p1 = lower_bound(x) * lower_bound(y)
    p2 = lower_bound(x) * upper_bound(y)
    p3 = upper_bound(x) * lower_bound(y)
    p4 = upper_bound(x) * upper_bound(y)
    return interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))

def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x divided
    by any value in y.

    Division is implemented as the multiplication of x by the reciprocal of y.

    >>> str_interval(div_interval(interval(-1, 2), interval(4, 8)))
    '-0.25 to 0.5'
    """
    assert lower_bound(y) != 0, "Found lower bound of y is zero"
    assert upper_bound(y) != 0, "Found upper bound of y is zero"
    reciprocal_y = interval(1/upper_bound(y), 1/lower_bound(y))
    return mul_interval(x, reciprocal_y)

def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y.
    >>> str_interval(sub_interval(interval(-1, 2), interval(4, 8)))
    '-9 to -2'
    """ 
    return interval( lower_bound(x) - upper_bound(y), upper_bound(x) - lower_bound(y))

def par1(r1, r2):
    return div_interval(mul_interval(r1, r2), add_interval(r1, r2))

def par2(r1, r2):
    one = interval(1, 1)
    rep_r1 = div_interval(one, r1)
    rep_r2 = div_interval(one, r2)
    return div_interval(one, add_interval(rep_r1, rep_r2))

# These two intervals give different results for parallel resistors:
print("Print an example of par1 and par2 giving different results:")
for example in [(interval(10,11),interval(33,34))]:
    r1, r2 = example

    print(par1(r1, r2))
    print(par2(r1, r2))


def multiple_references_explanation():
    return """The mulitple reference problem..."""

def multiplier_interval(x, m):
    if m >= 0:
        return interval( m*lower_bound(x), m*upper_bound(x) )
    else: 
        return interval( m*upper_bound(x), m*lower_bound(x) )

def offset_interval(x, m):
    return interval( m+lower_bound(x), m+upper_bound(x) )

def quadratic(x, a, b, c):
    """Return the interval that is the range of the quadratic defined by
    coefficients a, b, and c, for domain interval x.

    >>> str_interval(quadratic(interval(0, 2), -2, 3, -1))
    '-3 to 0.125'
    >>> str_interval(quadratic(interval(1, 3), 2, -3, 1))
    '0 to 10'
    """
    term1 = mul_interval(multiplier_interval(x, a), x)
    term2 = multiplier_interval(x, b)
    isSameside = (lower_bound(x) + b/2/a) * (higher_bound(x) +b/2/a)
    if isSmaeSide >= 0: # same side
    
    else:
        term12 = (term1, term2)
    return offset_interval(add_interval(term1, term2), c)

#def polynomial(x, c):
#    """Return the interval that is the range of the polynomial defined by
#    coefficients c, for domain interval x.
#
#    >>> str_interval(polynomial(interval(0, 2), [-1, 3, -2]))
#    '-3 to 0.125'
#    >>> str_interval(polynomial(interval(1, 3), [1, -3, 2]))
#    '0 to 10'
#    >>> str_interval(polynomial(interval(0.5, 2.25), [10, 24, -6, -8, 3]))
#    '18.0 to 23.0'
#    """
#    "*** YOUR CODE HERE ***"




