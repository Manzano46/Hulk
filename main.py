from engine.lexer.hulk_lexer import HulkLexer
from engine.language.tokens_type import hulk_tokens
from engine.language.grammar import G
from cmp.automata import State
from engine.lexer.regex import Regex
from engine.parser.lr1_parser_generator import LR1Parser
from cmp.evaluation import evaluate_reverse_parse


def pipeline(text):
    
    hulk_lexer = HulkLexer(hulk_tokens, G.EOF)
    tokens, errors = hulk_lexer(text)

    if errors :
        print('Errores de lexer: %s' % errors)
        return
    
    hulk_parser = LR1Parser(G)
    right_parse, operations = hulk_parser([token.token_type for token in tokens], True)
      
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    print(ast)
    
       
    
text = "print(\"hola \")"
print(pipeline(text))