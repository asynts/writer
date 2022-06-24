import math

def approximately_equal(lhs: any, rhs: any):
    return math.isclose(abs(lhs - rhs), 0)

def approximately_less(lhs: any, rhs: any):
    if lhs < rhs:
        return True

    return math.isclose(abs(lhs - rhs), 0)
