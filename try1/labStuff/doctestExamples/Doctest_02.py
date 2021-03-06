# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:11:06 2020

@author: eessrp
"""

def square(x):
    """Return the square of x.
    :param x: the value to be squared, or anything with the * operator defined
    :type x: real, int, complex or other
    :return: the square of x
    :rtype: the same type as the paramerter 

    >>> square(2)
    4
    >>> square(-2)
    4
    """
    return x * x 

if __name__ == '__main__':
    import doctest
    doctest.testmod()
 
xvalue=2.1
y = square(xvalue)    
print("(%g)^2=%g"%(xvalue,y))
