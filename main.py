from parser import infixToPostfix, tokenize, syntaxTreeFromRPN

# regex = '(0|1(01*0)*1)*'
regex = '(01*1)*1'
# regex = "(a|b)*abb"
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
print(dfa)

print(dfa.accepts('0'))
print(dfa.accepts('011'))
print(dfa.accepts('110'))
print(dfa.accepts('1001'))
print(dfa.accepts('1100'))
print(dfa.accepts('1111'))
print(dfa.accepts('100010'))

dfa.visualize()