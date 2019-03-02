from grammar import fromJSON

g = fromJSON('grammars/GNF.json')

print(g)
print(g.isInGNF())

# g.eliminateIdentity()

# g.eliminateLeftRecursion()

newg = g.toGNF()

print(newg)

print(newg.isInGNF())
