from engine.hulk_lexer import HulkLexer
from engine.tokens_type import hulk_tokens
from engine.grammar import G
from cmp.automata import State
from engine.regex import Regex

def pipeline(text):
    
    expr = '(a|b)*c'
    regex = Regex(expr)
    automata = regex.automaton()
    
    hulk_lexer = HulkLexer(hulk_tokens, G.EOF)
    tokens = hulk_lexer(text)
    
    print(tokens)
    
text = "print(\"hola \")"
print(pipeline(text))