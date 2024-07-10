from engine.lexer.hulk_lexer import HulkLexer
from engine.language.tokens_type import hulk_tokens
from engine.language.grammar import G
from cmp.automata import State
from engine.lexer.regex import Regex
from engine.parser.lr1_parser_generator import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from engine.parser.hulk_parser import HulkParser
import dill
import sys
from engine.semantic.hulk_semantic import hulk_semantic
from cmp.cil import get_formatter
from engine.code_generation.visitor import HulkToCILVisitor
from engine.language.interpreter import HulkInterpreter

def pipeline(text):
    
    hulk_lexer = HulkLexer(hulk_tokens, G.EOF)
    tokens, errors = hulk_lexer(text)

    if errors :
        print('Errores de lexer: %s' % errors)
        return
    
    try:
        with open('engine/lexer/hulk_lexer.pkl', 'rb') as hulk_lexer_dp:
            hulk_lexer = dill.load(hulk_lexer_dp)
    except:
        sys.setrecursionlimit(10000)
        hulk_lexer = HulkLexer(hulk_tokens, G.EOF)
        with open('engine/lexer/hulk_lexer.pkl', 'wb') as hulk_lexer_dp:
            dill.dump(hulk_lexer, hulk_lexer_dp)
            
    
    try:
        with open('engine/parser/hulk_parser.pkl', 'rb') as hulk_parser_dp:
            hulk_parser = dill.load(hulk_parser_dp)
    except:
        sys.setrecursionlimit(10000)
        hulk_parser = HulkParser()
        with open('engine/parser/hulk_parser.pkl', 'wb') as hulk_parser_dp:
            dill.dump(hulk_parser, hulk_parser_dp)
    
    print("TEXT")
    print()
    print(text)
    print('='*100)
    print()
    token = hulk_lexer(text)
    print("TOKENS")
    print(token)
    print()
    right_parse, operation = hulk_parser(token)
    ast = evaluate_reverse_parse(right_parse, operation, token)

    print()
    print(right_parse)
    print()
    print(operation)
    print()
    print(ast)
    print()
    print("="*100)
    
    ast, errors, context, scope = hulk_semantic(ast)
    
    print(errors)
    
    if errors != []:
        print("arregle los errores semanticos")
        
    
    hulk_interpreter = HulkInterpreter(context)
    hulk_interpreter.visit(ast)
    
    formatter = get_formatter()

    hulk_to_cil = HulkToCILVisitor(context)
    cil_ast = hulk_to_cil.visit(ast)
    formatter = get_formatter()
    print()
    print(formatter(cil_ast))
   
from tests.test_cases import test_cases  
pipeline(test_cases[12])