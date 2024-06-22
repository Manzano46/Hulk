from engine.automaton import NFA, DFA, nfa_to_dfa
from engine.automaton_operations import automata_union, automata_concatenation, automata_closure, automata_minimization
from cmp.pycompiler import Grammar
from cmp.utils import Token
from cmp.evaluation import evaluate_parse
from engine.lr1 import parser_lr1_generator

class Node:
    def evaluate(self):
        raise NotImplementedError()
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node
        
    def evaluate(self):
        value = self.node.evaluate() 
        return self.operate(value)
    
    @staticmethod
    def operate(value):
        raise NotImplementedError()
        
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()
    
EPSILON = 'epsilon'

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return NFA(states=2, finals=[1], transitions={(0, ''): [1] }, start=0)

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(states=2, finals=[1], transitions={(0, s): [1] }, start=0)

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)
    
class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)

def regex_grammar():
    G = Grammar()

    E = G.NonTerminal('E', True)
    T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
    pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')
    
    G._fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        '(': Token('(', opar),
        ')': Token(')', cpar),
        'ε': Token('ε', epsilon),
    }
    
    G._symbol = symbol

    E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]
    X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0], s[2])
    X %= G.Epsilon, lambda h,s: h[0]
    T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]
    Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0], s[1])
    Y %= G.Epsilon, lambda h,s: h[0]
    F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]
    Z %= star, lambda h,s: ClosureNode(h[0]), None
    Z %= G.Epsilon, lambda h,s: h[0]
    A %= opar + E + cpar, lambda h,s: s[2], None, None, None
    A %= symbol, lambda h,s: SymbolNode(s[1]), None 
    A %= epsilon, lambda h,s: EpsilonNode(EPSILON), None
    
    return G

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        # Your code here!!!
        if char in G._fixed_tokens.keys():
            tokens.append(G._fixed_tokens[char])
        else:
            tokens.append(Token(char, G._symbol))
        
    tokens.append(Token('$', G.EOF))
    return tokens

class Regex():
    def __init__(self, regular_exp, skip_whitespaces = False) -> None:
        self._regular_exp = regular_exp
        self._grammar = regex_grammar()
        self._parser = parser_lr1_generator(self._grammer)
        self._tokens = regex_tokenizer(regular_exp, self._grammer, skip_whitespaces=skip_whitespaces)
        self._right_parse = self._parser(self._tokens)
        self._ast = evaluate_parse(self._right_parse, self._tokens)
        self._nfa = self._ast.evaluate()
        self._dfa = nfa_to_dfa(self._nfa)

    def recognize(self, text):
        return self._dfa.recognize(text)

    def automaton(self):
        return self._dfa