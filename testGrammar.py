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
        path = 'grammars/GNF.json'
        g = fromJSON(path)
        X, H, K = g._toMatrix()
        self.assertEqual(X.mat.shape, (1, 2))
        self.assertEqual(H.mat.shape, (2, 2))
        self.assertEqual(K.mat.shape, (1, 2))

    def testToGNF(self):
        path = 'grammars/GNF.json'
        g = fromJSON(path)
        newG = g.toGNF()
        self.assertEqual(len(newG.nonterminals), len(g.nonterminals) + len(g.nonterminals) ** 2)
        self.assertEqual(len(newG.terminals), len(g.terminals))
        numPs = 0
        for _, rhs in newG.productions.items():
            numPs += len(rhs)
        self.assertEqual(numPs, 42)
