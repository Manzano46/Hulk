from engine.hulk_lexer import HulkLexer
from engine.tokens_type import hulk_tokens
from engine.grammar import G

def pipeline(text):
    
    hulk_lexer = HulkLexer(hulk_tokens, G.EOF)
    #hulk_lexer.automaton.graph().write_png('dfa.png')
    hulk_lexer.automaton
    tokens = hulk_lexer(text)
    
    #print(tokens)
    
text = "print"
print(pipeline(text))