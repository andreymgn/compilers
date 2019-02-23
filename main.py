from parser import infixToPostfix, tokenize, syntaxTreeFromRPN

tokens = tokenize("(a|b)*abb" + "#")
print(tokens)

rpn = infixToPostfix(tokens)
print(rpn)

st, positions = syntaxTreeFromRPN(rpn)

# s = st
# while s:
#     print('val={},nullable={},firstpos={},lastpost={},postition={}'.format(s.value, s.nullable, s.firstpos, s.lastpos, s.position))
#     s = s.left

followpos = st.getFollowpos()
print(followpos)

dfa = st.toDFA(followpos, positions, frozenset(['a', 'b']))
print(dfa)

print(dfa.accepts('abb'))
print(dfa.accepts('aabb'))
print(dfa.accepts('babb'))
print(dfa.accepts('abaabb'))
print(dfa.accepts('aaa'))

dfa.vizualize()