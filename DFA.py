from graphviz import Digraph

class DFA:
    def __init__(self, transitions, start, ends):
        self.transitions = transitions
        self.start = start
        self.ends = ends
    
    def accepts(self, s):
        state = self.start
        for ch in s:
            if ch not in self.transitions[state]:
                return False
            state = self.transitions[state][ch]
        
        return state in self.ends

    def visualize(self):
        def _frozensetStr(fs):
            s = '{'
            for v in fs:
                s += ' {}, '.format(v)
            return s + '}'

        f = Digraph('finite_state_machine', filename='fsm.gv')
        f.attr(rankdir='LR')

        f.attr('node', style='invis')
        f.node('start')

        f.attr('node', shape='doublecircle', style='solid')
        for end in self.ends:
            f.node(_frozensetStr(end))

        f.attr('node', shape='circle')
        f.edge('start', _frozensetStr(self.start), label='start')
        for s0, v in self.transitions.items():
            for ch, s1 in v.items():
                f.edge(_frozensetStr(s0), _frozensetStr(s1), label=ch)
        
        f.view()

    def minimize(self):
        pass