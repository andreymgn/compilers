import unittest

from grammar import fromJSON


class TestGrammar(unittest.TestCase):
    def testParse(self):
        testCases = {
            'grammars/dragon_book_immediate_left_recursion.json': {
                'numNonterminal': 3,
                'numTerminal': 5,
                'numProductions': 6
            },
            'grammars/dragon_book_indirect_left_recursion.json': {
                'numNonterminal': 2,
                'numTerminal': 4,
                'numProductions': 5
            },
            'grammars/GNF.json': {
                'numNonterminal': 2,
                'numTerminal': 4,
                'numProductions': 7
            },
            'grammars/2.4.19.json': {
                'numNonterminal': 3,
                'numTerminal': 2,
                'numProductions': 8
            }
        }

        for path, info in testCases.items():
            g = fromJSON(path)
            self.assertEqual(len(g.nonterminals), info['numNonterminal'])
            self.assertEqual(len(g.terminals), info['numTerminal'])
            numPs = 0
            for _, rhs in g.productions.items():
                numPs += len(rhs)
            self.assertEqual(numPs, info['numProductions'])

    def testEliminateLeftRecursion(self):
        testCases = {
            'grammars/dragon_book_immediate_left_recursion.json': {
                'numNonterminal': 5,
                'numTerminal': 5,
                'numProductions': 8
            },
            'grammars/dragon_book_indirect_left_recursion.json': {
                'numNonterminal': 3,
                'numTerminal': 4,
                'numProductions': 7
            }
        }

        for path, info in testCases.items():
            g = fromJSON(path)
            g.eliminateLeftRecursion()
            self.assertEqual(len(g.nonterminals), info['numNonterminal'])
            self.assertEqual(len(g.terminals), info['numTerminal'])
            numPs = 0
            for _, rhs in g.productions.items():
                numPs += len(rhs)
            self.assertEqual(numPs, info['numProductions'])

    def testToMatrix(self):
        testCases = {
            'grammars/GNF.json': {
                'X': (1, 2),
                'H': (2, 2),
                'K': (1, 2)
            },
            'grammars/2.4.19.json': {
                'X': (1, 3),
                'H': (3, 3),
                'K': (1, 3)
            }
        }
        for path, info in testCases.items():
            g = fromJSON(path)
            X, H, K = g._toMatrix()
            self.assertEqual(X.mat.shape, info['X'])
            self.assertEqual(H.mat.shape, info['H'])
            self.assertEqual(K.mat.shape, info['K'])

    def testToGNF(self):
        testCases = {
            'grammars/GNF.json': 42,
            'grammars/2.4.19.json': 48
        }
        for path, numProds in testCases.items():
            g = fromJSON(path)
            self.assertFalse(g.isInGNF())
            newG = g.toGNF()
            self.assertTrue(newG.isInGNF())
            self.assertEqual(len(newG.nonterminals),
                            len(g.nonterminals) + len(g.nonterminals) ** 2)
            self.assertEqual(len(newG.terminals), len(g.terminals))
            numPs = 0
            for _, rhs in newG.productions.items():
                numPs += len(rhs)
            self.assertEqual(numPs, numProds)

    def testFirst_1(self):
        testCase = {
            'E': set(['lparen', 'ident']),
            "E'": set(['plus', 'ϵ']),
            'T': set(['lparen', 'ident']),
            "T'": set(['mul', 'ϵ']),
            'F': set(['lparen', 'ident'])
        }
        g = fromJSON('grammars/g0.json')
        first = g.getFirst_1()
        for nt, fst in testCase.items():
            self.assertEqual(first[nt], fst)

    def testFollow_1(self):
        testCase = {
            'E': set(['$', 'rparen']),
            "E'": set(['$', 'rparen']),
            'T': set(['$', 'rparen', 'plus']),
            "T'": set(['$', 'rparen', 'plus']),
            'F': set(['$', 'rparen', 'plus', 'mul'])
        }
        g = fromJSON('grammars/g0.json')
        first = g.getFirst_1()
        follow = g.getFollow_1(first)
        for nt, flw in testCase.items():
            self.assertEqual(follow[nt], flw)
