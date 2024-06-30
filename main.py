from engine.hulk_lexer import HulkLexer
from engine.tokens_type import hulk_tokens
from engine.grammar import G
from cmp.automata import State
from engine.regex import Regex
from engine.lr1_parser_generator import LR1Parser
from cmp.evaluation import evaluate_reverse_parse


def pipeline(text):
    
    hulk_lexer = HulkLexer(hulk_tokens, G.EOF)
    tokens = hulk_lexer(text)
    
    hulk_parser = LR1Parser(G)
    right_parse, operations = hulk_parser([token.token_type for token in tokens], True)
      
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    print(ast)
    
       
    
text = "print(\"hola \")"
print(pipeline(text))