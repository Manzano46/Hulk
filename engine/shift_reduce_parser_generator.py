from cmp.pycompiler import Grammar
from cmp.pycompiler import Item
from cmp.automata import State, lr0_formatter
from engine.firsts_follows import compute_firsts, compute_follows


# NOTA: use `symbol.Name` al hacer las transiciones, no directamente `symbol`.
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
        operations = []
        count = 1
        while True:
            #print(stack)
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:], count)
            count+=1
                
            #lookahead = lookahead.Name
            
            if (state, lookahead) not in self.action:
                raise Exception(f'No se esperaba el token {lookahead}')
            
            action, tag = self.action[state, lookahead]
            if action == ShiftReduceParser.SHIFT:
                stack.append(lookahead)
                stack.append(tag)
                operations.append(action)   
            
                cursor += 1

            elif action == ShiftReduceParser.REDUCE:
                #print(tag)
                left, right = tag
                for i in right:
                    stack.pop()
                new_state = self.goto[stack[-1], left]
                stack.append(left)
                stack.append(new_state)
                output.append(tag)
                operations.append(action) 

            elif action == ShiftReduceParser.OK:
                return output, operations

            else:
                raise Exception('Invalid')
