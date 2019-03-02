import unittest

from matrix import Matrix, mul
from orderedSet import OrderedSet


class MatrixTest(unittest.TestCase):
    def testConstruct(self):
        m = Matrix([[['1', '2'], ['2']], [['3'], ['3', '4']]])
        self.assertEqual(m.mat.shape, (2, 2))

    def testDot(self):
        lhs = Matrix([[['1', '2'], ['2']], [['3'], ['3', '4']]])
        rhs = Matrix([[['1', '2'], ['2']], [['3'], ['3', '4']]])
        dot = lhs.dot(rhs)
        result = Matrix([[['11', '12', '21', '22', '23'], ['12', '22', '23', '24']],
                         [['31', '32', '33', '43'], ['32', '33', '34', '43', '44']]])
        self.assertEqual(dot.mat.shape, (2, 2))
        self.assertTrue((dot.mat == result.mat).all())

    def testMul(self):
        lhs = OrderedSet(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        rhs = OrderedSet(['1', '2', '3', '4', '5', '6', '7', '8'])
        prod = mul(lhs, rhs)
        result = OrderedSet(['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                             'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
                             'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
                             'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
                             'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
                             'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
                             'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
                             'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'])
        self.assertEqual(prod, result)
