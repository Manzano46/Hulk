import pydot
from cmp.utils import ContainerSet

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'epsilon' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass
        

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):     
        if symbol in self.transitions[self.current].keys():
            self.current = self.transitions[self.current][symbol][0]
            return True
        return False
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self._reset()
        for symbol in string:
            
            if not self._move(symbol):
                return False
        
        return self.current in self.finals
    
def move(automaton, states, symbol):
    moves = set()
    for state in states:
    
        if symbol in automaton.transitions[state].keys():
            moves = moves.union(set(automaton.transitions[state][symbol]))
      
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] 
    closure = { s for s in states } 
    
    while pending:
        state = pending.pop()
        aux = move(automaton,[state],'')
        dif = aux - closure
        closure.update(dif)
        pending += dif
                
    return ContainerSet(*closure)

def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            _move = move(automaton, state, symbol)
            _closure = epsilon_closure(automaton, _move)

            if len(_closure) == 0:
                continue
            if _closure not in states:
                _closure.id = len(states)
                _closure.is_final = any(s in automaton.finals for s in _closure)
                pending.append(_closure)
                states.append(_closure)
            else:
                _closure.id = states.index(_closure)
            

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = _closure.id
                pass
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa