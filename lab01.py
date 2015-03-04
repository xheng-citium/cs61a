def my_email():
    """Return your email address as a string.

    >>> my_email() != 'oski@berkeley.edu'
    True
    """
    return 'xheng@citiumadvisors.com'

from operator import add, mul

def twenty_fourteen():
    """Come up with the most creative expression that evaluates to 2014, 
    using only numbers and the functions add(. . .) and mul(. . .).

    >>> twenty_fourteen()
    2014
    """
    y = add( mul(2, 1000), add(mul(0, 100), add(mul(1, 10), 4)))
    return y





