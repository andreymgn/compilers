import json
from collections import defaultdict

import numpy as np

from matrix import Matrix
from orderedSet import OrderedSet


class Grammar:
    """Context-free grammar
    """
    def __init__(self, nonterminals, terminals, productions, start):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start = start

    def __str__(self):
        prods = self._prodsToStr()
        return 'Grammar with\nnonterminals: {},\
            \nterminals: {},\
            \nproductions: \n{},\
            \nstart: {}'\
            .format(self.nonterminals, self.terminals, prods, self.start)

    def _prodsToStr(self):
        result = []
        for lhs, rhs in self.productions.items():
            s = '{} -> '.format(lhs)
            for i, prod in enumerate(rhs):
                if i != 0:
                    s += ' | '
                for symbol in prod:
                    if symbol[1]:
                        s += self.terminals[symbol[0]] + ' '
                    else:
                        s += symbol[0] + ' '
            result.append(s)
        return '\n'.join(result)

    def eliminateIdentity(self):
        # remove rules like A -> A
        updatedProductions = {}
        for lhs, rhs in self.productions.items():
            newRhs = []
            for prod in rhs:
                if len(prod) != 1 or prod[0] != lhs:
                    newRhs.append(prod)
            updatedProductions[lhs] = newRhs
        for lhs, rhs in updatedProductions.items():
            self.productions[lhs] = rhs

    def eliminateImmediateLeftRecursion(self, lhs=None):
        if lhs is None:
            productions = self.productions
        else:
            productions = {lhs: self.productions[lhs]}
        updatedProductions = {}
        for lhs, rhs in productions.items():
            alpha = []
            beta = []
            lhsPrime = lhs + "1"
            for prod in rhs:
                if prod[0][0] == lhs:
                    alpha.append(prod[1:] + [(lhsPrime, False)])
                elif prod[0][0] == 'ϵ':
                    beta.append([(lhsPrime, False)])
                else:
                    beta.append(prod + [(lhsPrime, False)])
            if len(alpha) != 0:
                # add new nonterminal lhs'
                self.nonterminals.append(lhsPrime)
                updatedProductions[lhs] = beta
                updatedProductions[lhsPrime] = alpha + [[('ϵ', False)]]
        for lhs, rhs in updatedProductions.items():
            self.productions[lhs] = rhs

    def eliminateLeftRecursion(self):
        nt = self.nonterminals
        for i in range(len(nt)):
            for j in range(i):
                updatedProductions = defaultdict(list)
                for lhs, rhs in self.productions.items():
                    for prod in rhs:
                        if lhs == nt[i]:
                            if prod[0][0] == nt[j]:
                                for delta in self.productions[nt[j]]:
                                    newProd = delta + prod[1:]
                                    updatedProductions[lhs].append(newProd)
                            else:
                                updatedProductions[lhs].append(prod)
                for lhs, rhs in updatedProductions.items():
                    self.productions[lhs] = rhs
            self.eliminateImmediateLeftRecursion(nt[i])

    def toGNF(self):
        """Convert grammar to Greibach normal form
        """
        # 1) convert to matrix form: X * H + K,
        # where X is a row vector of nonterminals,
        # H is a matrix of productions which start with nonterminal
        # K is a row vector of productions which start with terminal
        # for example look at [1] starting on page 20
        # [1] https://www.cis.upenn.edu/~jean/old511/html/cis51108sl4b.pdf

        X, H, K = self._toMatrix()

        # 2) write system of equations
        # { X = K * Y + K
        # { Y = H * Y + H
        # where Y is a matrix of new nonterminals with size same as H
        Y = [[[(('Y{}{}'.format(j, i), False),)]
              for i in range(H.mat.shape[0])] for j in range(H.mat.shape[1])]
        Y = Matrix(Y)

        # 3) calculate X from step 2
        # substitute nonterminals in matrix H with calculated X values
        # and get matrix L
        # the new system is:
        # { X = K * Y + K
        # { Y = L * Y + L
        # calculate X, calculate Y
        # convert these matrices to one grammar

        xCalc = K.dot(Y).add(K)
        subs = {}
        for i, nt in enumerate(self.nonterminals):
            subs[nt] = xCalc.mat[0][i]

        L = H
        for i, row in enumerate(H.mat):
            for j, val in enumerate(row):
                newCell = []
                for tup in val:
                    if tup[0][0] in subs:
                        for sub in subs[tup[0][0]]:
                            newCell.append(sub + tup[1:])
                    else:
                        newCell.append(tup)
                L.mat[i, j] = OrderedSet(newCell)

        yCalc = L.dot(Y).add(L)

        terminals = self.terminals
        nonterminals = self.nonterminals + \
            ['Y{}{}'.format(j, i)
             for i in range(H.mat.shape[0]) for j in range(H.mat.shape[1])]
        productions = {}
        start = self.start
        for i, oldNT in enumerate(self.nonterminals):
            productions[oldNT] = xCalc.mat[0][i]
        for i, row in enumerate(yCalc.mat):
            for j, val in enumerate(row):
                lhs = 'Y{}{}'.format(j, i)
                productions[lhs] = val

        return Grammar(nonterminals, terminals, productions, start)

    def isInGNF(self):
        for _, rhs in self.productions.items():
            for prod in rhs:
                if not prod[0][1]:
                    return False
        return True

    def _toMatrix(self):
        X = []
        H = [[[] for _ in self.nonterminals] for _ in self.nonterminals]
        ntToIdx = {}
        for i, nt in enumerate(self.nonterminals):
            ntToIdx[nt] = i

        K = [[] for _ in self.nonterminals]
        for i, nt in enumerate(self.nonterminals):
            X.append(nt)
            for prod in self.productions[nt]:
                if prod[0][1]:
                    K[ntToIdx[nt]].append(tuple(prod))
                else:
                    row = ntToIdx[nt]
                    col = ntToIdx[prod[0][0]]
                    H[row][col].append(tuple(prod[1:]))
        K = Matrix(K, transpose=True, isVector=True)
        K.mat = np.expand_dims(K.mat, axis=1)
        K.mat = K.mat.T
        return Matrix(X, transpose=True), Matrix(H, transpose=True), K


def fromJSON(filename):
    with open(filename) as f:
        data = json.load(f)
    nts = data['nonterminals']

    ts = {}
    for term in data['terminals']:
        ts[term['name']] = term['spelling']

    ps = defaultdict(list)
    for p in data['productions']:
        lhs = p['lhs']
        rhs = []
        for symbol in p['rhs']:
            rhs.append((symbol['name'], symbol['isTerminal']))
        ps[lhs].append(rhs)

    start = data['start']

    return Grammar(nts, ts, ps, start)
