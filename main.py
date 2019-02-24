from parser import infixToPostfix, tokenize, syntaxTreeFromRPN
from DFA import DFA

regex = '(0|1(01*0)*1)*'
# regex = '(01*1)*1'
# regex = "(a|b)*abb"
# regex = "(a|b)*"
# regex = "(a*|b*)*"

def showAccepts(regex, testStr):
    sigma = set(regex) - set('()|*')
    tokens = tokenize(regex + '#')

    rpn = infixToPostfix(tokens)
    st, positions = syntaxTreeFromRPN(rpn)
    followpos = st.getFollowpos()

    dfa = st.toDFA(followpos, positions, sigma)
    print(dfa.accepts(testStr))

    dfa.visualize()

    eqCls = dfa.findEquivalenceClasses(sigma)
    dfa.mergeEquivalentStates(eqCls)
    dfa.visualize(fname='fsm1.gv')


def showMinimization():
    tt = {
        frozenset(['a']): {
            '0': frozenset(['b']),
            '1': frozenset(['c'])
        },
        frozenset(['b']): {
            '0': frozenset(['a']),
            '1': frozenset(['d'])
        },
        frozenset(['c']): {
            '0': frozenset(['e']),
            '1': frozenset(['f'])
        },
        frozenset(['d']): {
            '0': frozenset(['e']),
            '1': frozenset(['f'])
        },
        frozenset(['e']): {
            '0': frozenset(['e']),
            '1': frozenset(['f'])
        },
        frozenset(['f']): {
            '0': frozenset(['f']),
            '1': frozenset(['f'])
        }
    }
    sigma = set(['0', '1'])
    start = 'a'
    end = set([frozenset(['c']), frozenset(['d']), frozenset(['e'])])
    dfa = DFA(tt, start, end)

    dfa.visualize()

    eqCls = dfa.findEquivalenceClasses(sigma)
    dfa.mergeEquivalentStates(eqCls)
    dfa.visualize(fname='fsm1.gv')

showMinimization()