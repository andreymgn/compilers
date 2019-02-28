from collections import namedtuple, defaultdict

import json

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
        return 'Grammar with\nnonterminals: {},\nterminals: {},\nproductions: {},\nstart: {}'.format(self.nonterminals, self.terminals, prods, self.start)

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
        return result

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
                                    updatedProductions[lhs].append(delta + prod[1:])
                            else:
                                updatedProductions[lhs].append(prod)
                for lhs, rhs in updatedProductions.items():
                    self.productions[lhs] = rhs
            self.eliminateImmediateLeftRecursion(nt[i])


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
