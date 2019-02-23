from graphviz import Digraph

class DFA:
    def __init__(self, transitions: dict, start: frozenset, end:frozenset):
        self.transitions = transitions
        self.start = start
        self.end = end
    
    def accepts(self, s: str) -> bool:
        state = self.start
        for ch in s:
            state = self.transitions[state][ch]
        
        return state == self.end

    def vizualize(self) -> None:
        def _frozensetStr(fs: frozenset) -> str:
            s = '{'
            for v in fs:
                s += ' {}, '.format(v)
            return s + '}'

        f = Digraph('finite_state_machine', filename='fsm.gv')
        f.attr(rankdir='LR')

        f.attr('node', style='invis')
        f.node('start')

        f.attr('node', shape='doublecircle', style='default')
        f.node(_frozensetStr(self.end))

        f.attr('node', shape='circle')
        f.edge('start', _frozensetStr(self.start), label='start')
        for s0, v in self.transitions.items():
            for ch, s1 in v.items():
                f.edge(_frozensetStr(s0), _frozensetStr(s1), label=ch)
        
        f.view()

    

