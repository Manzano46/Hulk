from engine.Automaton.automaton import NFA, DFA, nfa_to_dfa
from engine.Automaton.automaton_operations import automata_union, automata_concatenation, automata_closure, automata_minimization
from cmp.pycompiler import Grammar
from cmp.utils import Token
from cmp.evaluation import evaluate_reverse_parse
from engine.Parser.lr1_parser_generator import LR1Parser

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

    S = G.NonTerminal('S', True)
    E, T, F, A = G.NonTerminals('E T F A')
    pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')
    
    G._fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        '(': Token('(', opar),
        ')': Token(')', cpar),
        'ε': Token('ε', epsilon),
    }
    
    G._symbol = symbol

    S %= E, lambda h,s: s[1]
    E %= E + pipe + T, lambda h,s: UnionNode(s[1], s[3])
    E %= T, lambda h,s: s[1]
    T %= T + F, lambda h,s: ConcatNode(s[1], s[2])
    T %= F, lambda h,s: s[1]
    F %= A + star, lambda h,s: ClosureNode(s[1])
    F %= A, lambda h,s: s[1]
    A %= opar + E + cpar, lambda h,s: s[2]
    A %= symbol, lambda h,s: SymbolNode(s[1])
    A %= epsilon, lambda h,s: EpsilonNode(s[1])
    
    
    return G

def regex_tokenizer(text, G : Grammar, skip_whitespaces=True):
    tokens = []
    #print(text, "tokeni")
    force = False
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        if not force and char == '\\':
            force  = True
            continue
        
        token = G._fixed_tokens.get(char,None)
        
        if token is None or force:
            token = Token(char, G._symbol)
            force = False
        
        tokens.append(token)
        
    tokens.append(Token('$', G.EOF))
    #print(tokens)
    return tokens

_grammar = regex_grammar()
_parser = LR1Parser(_grammar)

class Regex():
    def __init__(self, regular_exp, skip_whitespaces = False) -> None:
        self._regular_exp = regular_exp
      
        self._tokens = regex_tokenizer(regular_exp, _grammar, skip_whitespaces=skip_whitespaces)
        
        self._right_parse, self._operations = _parser([token.token_type for token in self._tokens], True)
      
        self._ast = evaluate_reverse_parse(self._right_parse, self._operations, self._tokens)
       
        self._nfa = self._ast.evaluate()
        self._nfa
        self._dfa = nfa_to_dfa(self._nfa)
        #self._dfa.graph().write_png('dfa.png')
        
       
    def recognize(self, text):
        return self._dfa.recognize(text)

    def automaton(self):
        return self._dfa