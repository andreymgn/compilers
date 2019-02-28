from grammar import fromJSON

g = fromJSON('grammars/dragon_book_indirect_left_recursion.json')

# print(g)

g.eliminateIdentity()

# print(g)

g.eliminateLeftRecursion()

print(g)