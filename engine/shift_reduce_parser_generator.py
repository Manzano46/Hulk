from cmp.pycompiler import Grammar
from cmp.pycompiler import Item
from cmp.automata import State, lr0_formatter
from engine.firsts_follows import compute_firsts, compute_follows


# NOTA: use `symbol.Name` al hacer las transiciones, no directamente `symbol`.

def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        print(current_item)
        if current_item.IsReduceItem:
            continue
        
        next_item = current_item.NextItem()
        next_state = State(next_item, True)
        current_state = visited[current_item]
        
        pending.append(next_item)
        visited[next_item] = next_state
        current_state.add_transition(current_item.NextSymbol.Name, next_state)
        
        if current_item.NextSymbol.IsNonTerminal:
            for prod in current_item.NextSymbol.productions:
                item = Item(prod, 0)
                try:
                    visited[item]
                except KeyError:
                    pending.append(item)
                    next_state = State(item, True)
                    visited[item] = next_state
                current_state.add_epsilon_transition(visited[item])
            
    return automaton

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        count = 1
        while True:
            print(stack)
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:], count)
            count+=1
                
            lookahead = lookahead.Name
            if (state, lookahead) not in self.action.keys():
                raise Exception(f'No se esperaba el token {lookahead}')
            
            action, tag = self.action[state, lookahead]
            if action == ShiftReduceParser.SHIFT:
                stack.append(lookahead)
                stack.append(tag)
                cursor += 1

            elif action == ShiftReduceParser.REDUCE:
                left, right = production = self.G.Productions[tag]
                count_delete = 2 * len(right)
                for i in range(count_delete):
                    stack.pop()
                new_state = self.goto[stack[-1], left.Name]
                stack.append(left.Name)
                stack.append(new_state)
                output.append(production)

            elif action == ShiftReduceParser.OK:
                return output

            else:
                raise Exception('Invalid')


class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state                
                if not item.IsReduceItem:
                    symbol =  item.NextSymbol
                    if symbol.IsTerminal:                        
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata No Determinista.'
                            self._register(self.action,
                                        (idx, item.NextSymbol.Name),
                                        (ShiftReduceParser.SHIFT, node_transition[0].idx))
                    else:
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata no determinista.'
                            self._register(self.goto,
                                        (idx, item.NextSymbol.Name),
                                        (node_transition[0].idx))                    
                else:
                    left, right = production = item.production
                    k = G.Productions.index(production)
                    if left.Name == G.startSymbol.Name:
                        k = G.Productions.index(item.production)
                        self._register(self.action,
                            (idx, G.EOF.Name),
                            (ShiftReduceParser.OK, k))                    
                    for terminal in follows[left]:
                        if terminal == G.EOF and left.Name == G.startSymbol.Name:
                            continue
                        self._register(self.action,
                                    (idx, terminal.Name),
                                    (ShiftReduceParser.REDUCE, k))
    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value