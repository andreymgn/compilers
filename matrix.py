import numpy as np

from orderedSet import OrderedSet


class Matrix:
    """matrix where sum defined as union
    and multiplication defined as concatenation
    the elements are sets of strings
    """
    def __init__(self, elements, transpose=False, isVector=False):
        if isVector:
            els = [OrderedSet(x) for x in elements]
        else:
            els = [[OrderedSet(x) for x in row] for row in elements]
        self.mat = np.array(els, dtype=object)
        if transpose:
            self.mat = self.mat.T

    def dot(self, rhs):
        assert self.mat.shape[1] == rhs.mat.shape[0]
        els = [[OrderedSet([])
               for _ in range(rhs.mat.shape[1])]
               for _ in range(self.mat.shape[0])]
        result = np.array(els, dtype=object)
        for i in range(self.mat.shape[0]):
            for j in range(rhs.mat.shape[1]):
                for k in range(self.mat.shape[1]):
                    m = mul(self.mat[i, k], rhs.mat[k, j])
                    result[i, j] = add(result[i, j], m)
        m = Matrix([])
        m.mat = result
        return m

    def add(self, rhs):
        assert self.mat.shape == rhs.mat.shape
        els = [[OrderedSet([])
               for _ in range(self.mat.shape[1])]
               for _ in range(self.mat.shape[0])]
        result = np.array(els, dtype=object)
        for i in range(self.mat.shape[0]):
            for j in range(self.mat.shape[1]):
                result[i, j] = add(self.mat[i, j], rhs.mat[i, j])
        m = Matrix([])
        m.mat = result
        return m


def add(lhs, rhs):
    """lhs and rhs are sets
    and addition is defined to be union of these sets
    """
    return lhs | rhs


def mul(lhs, rhs):
    """lhs and rhs are sets
    multiplication is concatenation
    see: https://en.wikipedia.org/wiki/Concatenation#Concatenation_of_sets_of_strings
    """
    return OrderedSet([a + b for a in lhs for b in rhs])
