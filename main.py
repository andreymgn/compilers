from parser import infixToPostfix, tokenize, syntaxTreeFromRPN
from DFA import DFA

# regex = '(0|1(01*0)*1)*'
# regex = '(01*1)*1'
regex = "(a|b)*abb"
# regex = "(a|b)*"
# regex = "(a*|b*)*"
sigma = set(regex) - set('()|*')

tokens = tokenize(regex + '#')
print(tokens)

rpn = infixToPostfix(tokens)
print(rpn)

st, positions = syntaxTreeFromRPN(rpn)

followpos = st.getFollowpos()
print(followpos)

dfa = st.toDFA(followpos, positions, sigma)

# tt = {
#     frozenset(['a']): {
#         '0': frozenset(['b']),
#         '1': frozenset(['c'])
#     },
#     frozenset(['b']): {
#         '0': frozenset(['a']),
#         '1': frozenset(['d'])
#     },
#     frozenset(['c']): {
#         '0': frozenset(['e']),
#         '1': frozenset(['f'])
#     },
#     frozenset(['d']): {
#         '0': frozenset(['e']),
#         '1': frozenset(['f'])
#     },
#     frozenset(['e']): {
#         '0': frozenset(['e']),
#         '1': frozenset(['f'])
#     },
#     frozenset(['f']): {
#         '0': frozenset(['f']),
#         '1': frozenset(['f'])
#     }
# }

# start = 'a'

# end = set([frozenset(['c']), frozenset(['d']), frozenset(['e'])])

# dfa = DFA(tt, start, end)

# print(dfa.accepts('0'))
# print(dfa.accepts('011'))
# print(dfa.accepts('110'))
# print(dfa.accepts('1001'))
# print(dfa.accepts('1100'))
# print(dfa.accepts('1111'))
# print(dfa.accepts('100010'))

#dfa.visualize()

print('a')
eqCls = dfa.findEquivalenceClasses(sigma)
for p in eqCls:
    print(p)

dfa.mergeEquivalentStates(eqCls)

print(dfa.ends)

dfa.visualize()