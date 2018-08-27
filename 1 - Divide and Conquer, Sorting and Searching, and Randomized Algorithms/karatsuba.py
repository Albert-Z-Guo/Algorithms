# reference: Algorithms Illuminated: Part 1: The Basics Chapter 1.3

from math import ceil # math.ceil(x) returns the ceiling of x as a float, the smallest integer value greater than or equal to x.
from math import log2 # math.log2(x) returns the base-2 logarithm of x.

BASE = 10

# method to select high dights
def _high_half(s):
    '''
    Note that in the trial example below in the main function the halves of
    3141592653589793238462643383279502884197169399375105820974944592 are:
    31415926535897932384626433832795 and 02884197169399375105820974944592
    where 0 at the front of 02884197169399375105820974944592 must be taken care of.
    s : positive integer in string format
    '''
    len_half = int(len(s) / 2)
    return s[:len_half]

# method to select low dights
def _low_half(s):
    '''
    s : positive integer in string format
    '''
    len_half = int(len(s) / 2)
    return s[len_half:]

# recursive integer multiplication method
def multiply(x, y):
    '''
    x : n-digit positive integer in string format
    y : n-digit positive integer in string format
    n is a power of 2
    '''

    # base case
    '''
    Note that for recursive integer multiplication,
    x and y always have the same digit length.
    '''
    if int(x) < 10 and int(y) < 10:
        return int(x) * int(y)

    x_H = _high_half(x)
    x_L = _low_half(x)
    y_H = _high_half(y)
    y_L = _low_half(y)

    a = multiply(x_H, y_H)
    d = multiply(x_L, y_L)
    e = multiply(x_H, y_L) + multiply(x_L, y_H)

    '''
    Note that unlike the built-in ** operator,
    math.pow() converts both its arguments to type float.
    Use ** or the built-in pow() function for computing exact integer powers.
    '''
    n = len(str(x))
    return int(a * (pow(BASE, n)) + e * pow(BASE, int(n / 2)) + d)

# karatsuba multiplication method
def karatsuba(x, y):
    '''
    x : n-digit positive integer in string format
    y : n-digit positive integer in string format
    n is a power of 2
    '''

    # base case
    '''
    Note that for karatsuba multiplication,
    x and y may have different digit lengths.
    '''
    if int(x) < 10 or int(y) < 10:
        return int(x) * int(y)

    '''
    Note that we may have examples like karatsuba('123', '23')
    when calculating e, as mentioned below.
    Therefore, we need to add appropriate number of '0' in front of '123' and '23'
    to make sure x and y in karatsuba(x, y) are of digits in power of 2.
    '''
    len_max = max(len(x), len(y))
    len_expected = pow(2, ceil(log2(len_max)))
    if len(x) != len_expected:
        x = '0' * (len_expected - len(x)) + x
    if len(y) != len_expected:
        y = '0' * (len_expected - len(y)) + y

    x_H = _high_half(x)
    x_L = _low_half(x)
    y_H = _high_half(y)
    y_L = _low_half(y)

    a = karatsuba(x_H, y_H)
    d = karatsuba(x_L, y_L)
    e = karatsuba(str(int(x_H) + int(x_L)), str(int(y_H) + int(y_L))) - a - d

    n = len(x)
    return int(a * (pow(BASE, n)) + e * pow(BASE, int(n / 2)) + d)

if __name__ == "__main__":
    # reference: http://www.javascripter.net/math/calculators/100digitbigintcalculator.htm
    correct_answer = '8539734222673567065463550869546574495034888535765114961879601127067743044893204848617875072216249073013374895871952806582723184'

    print('RecIntMult Answer:', multiply('3141592653589793238462643383279502884197169399375105820974944592','2718281828459045235360287471352662497757247093699959574966967627'))
    print('karatsuba Answer :', karatsuba('3141592653589793238462643383279502884197169399375105820974944592','2718281828459045235360287471352662497757247093699959574966967627'))
    print('Correct Answer   :', correct_answer)
