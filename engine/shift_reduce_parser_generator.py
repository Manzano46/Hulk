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

    def __call__(self, w, get_shift_reduce=False):
        stack = [0]
        cursor = 0
        output = []
        operations = []

        while True:
            state = stack[-1]
            lookahead = w[cursor]

            if self.verbose:
                print(stack, '<---||--->', w[cursor:])

            if (state, lookahead) not in self.action:
                print((state, lookahead))
                print("Error. Aborting...")
                return None

            action, tag = self.action[(state, lookahead)]

            if action == self.SHIFT:
                operations.append(self.SHIFT)
                stack += [lookahead, tag]
                cursor += 1
            elif action == self.REDUCE:
                operations.append(self.REDUCE)
                output.append(tag)
                head, body = tag
                for symbol in reversed(body):
                    stack.pop()
                    assert stack.pop() == symbol
                state = stack[-1]
                goto = self.goto[(state, head)]
                stack += [head, goto]
            elif action == self.OK:
                stack.pop()
                assert stack.pop() == self.G.startSymbol
                assert len(stack) == 1
                return output if not get_shift_reduce else (output, operations)
            else:
                raise Exception('Invalid action!!!')
