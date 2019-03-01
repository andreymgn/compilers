from grammar import fromJSON

g = fromJSON('grammars/GNF.json')

# g.eliminateIdentity()

# print(g)

# g.eliminateLeftRecursion()

newg = g.toGNF()

# print(newg.terminals)

# print(newg.productions)

print(newg)