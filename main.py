from grammar import fromJSON

g = fromJSON('grammars/g0.json')

g.eliminateIdentity()

g.eliminateLeftRecursion()

print()
print(g)

first = g.getFirst_1()
print(first)

print()
follow = g.getFollow_1(first)
print(follow)
