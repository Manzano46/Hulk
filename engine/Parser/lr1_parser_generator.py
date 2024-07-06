from cmp.pycompiler import Grammar
from cmp.pycompiler import Item
from cmp.utils import ContainerSet
from engine.Parser.firsts_follows import compute_firsts, compute_local_first
from engine.Parser.shift_reduce_parser_generator import ShiftReduceParser
from pandas import DataFrame

def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
    for x in item.Preview():
        aux = compute_local_first(firsts, x)
        lookaheads.update(aux)
    
    assert not lookaheads.contains_epsilon
    
    ans = []
    for x in next_symbol.productions:
        ans.append(Item(x,0, lookaheads))
    return ans

def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        
        lookaheads.update(item.lookaheads)
        
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)
        
    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

from cmp.automata import State, multiline_formatter

'''
def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    clousure = closure_lr1(start, firsts)
    automaton = State(frozenset(clousure), True)
    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]
        for symbol in G.terminals + G.nonTerminals:
            goto_clousure = closure_lr1(current, firsts)
            goto_result = goto_lr1(goto_clousure, symbol, just_kernel=True)

            if not goto_result:
                continue

            next_state = visited.get(goto_result)
            if next_state is None:
                goto_clousure = closure_lr1(goto_result, firsts)
                next_state = visited[goto_result] = State(frozenset(goto_clousure), True)
                pending.append(goto_result)
            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton
'''

def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = {G.EOF}

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = frozenset(closure_lr1(start, firsts))
    automaton = State(closure, True)

    pending = [closure]
    visited = {closure: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            goto = frozenset(goto_lr1(current, symbol, firsts))

            if len(goto) > 0:
                if goto not in visited:
                    visited[goto] = State(goto, True)
                    pending.append(goto)

                current_state.add_transition(symbol.Name, visited[goto])

    automaton.set_formatter(multiline_formatter)
    return automaton
    
    
class LR1Parser(ShiftReduceParser):
   def _build_parsing_table(self):
      G = self.G.AugmentedGrammar(True)
      automaton = build_LR1_automaton(G)
      for idx, node in enumerate(automaton):
         if self.verbose:
               print(idx, '\t', '\n\t'.join(str(x) for x in node.state), '\n')
         node.idx = idx
      
      for node in automaton:
         current_idx = node.idx
         for item in node.state:
               if item.IsReduceItem:
                  production = item.production
                  if production.Left == G.startSymbol:
                     self._register(self.action, (current_idx, G.EOF), (self.OK, None))
                  else:
                     for lookahead in item.lookaheads:
                           self._register(self.action, (current_idx, lookahead), (self.REDUCE, production))
               else:
                  next_symbol = item.NextSymbol
                  node_transition_idx = node.get(next_symbol.Name).idx
                  if next_symbol.IsTerminal:
                     self._register(self.action, (current_idx, next_symbol), (self.SHIFT, node_transition_idx))
                  else:
                     self._register(self.goto, (current_idx, next_symbol), node_transition_idx)

   @staticmethod
   def _register(table, key, value):
      assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
      table[key] = value
                
def encode_value(value):
    try:
        action, tag = value
        if action == ShiftReduceParser.SHIFT:
            return 'S' + str(tag)
        elif action == ShiftReduceParser.REDUCE:
            return repr(tag)
        elif action ==  ShiftReduceParser.OK:
            return action
        else:
            return value
    except TypeError:
        return value

def table_to_dataframe(table):
    d = {}
    for (state, symbol), value in table.items():
        value = encode_value(value)
        try:
            d[state][symbol] = value
        except KeyError:
            d[state] = { symbol: value }

    return DataFrame.from_dict(d, orient='index', dtype=str)