import sys
from typing import List

#import dill

import engine.language.grammar as grammar
from engine.lexer.hulk_lexer import TokenType
from engine.parser.lr1_parser_generator import LR1Parser
from cmp.utils import Token


class HulkParser(LR1Parser):
    def __init__(self):
        super().__init__(grammar.G)
        self.tokens_terminals_map = {
        '$' : grammar.G.EOF,
        TokenType.EOF: grammar.G.EOF,
        grammar.G.EOF: grammar.G.EOF,
        TokenType.OPAR: grammar.opar,
        TokenType.CPAR: grammar.cpar,
        TokenType.OPCOR: grammar.opcor,
        TokenType.CLCOR: grammar.clcor,
        TokenType.OPCUR: grammar.opcur,
        TokenType.CLCUR: grammar.clcur,
        TokenType.COMMA: grammar.comma,
        TokenType.DOT: grammar.dot,
        TokenType.COLON: grammar.colon,
        TokenType.SEMI: grammar.semi,
        TokenType.ARROW: grammar.arrow,
        TokenType.DOUBLE_OR: grammar.double_or,
        TokenType.EQUAL: grammar.equal,
        TokenType.DESTRUCTIVE: grammar.destructive,

        TokenType.IDX: grammar.idx,
        TokenType.STRING: grammar.string,
        TokenType.NUM: grammar.num,
        TokenType.BOOLEAN: grammar.boolean,

        # Arithmetic operators
        TokenType.PLUS: grammar.plus,
        TokenType.MINUS: grammar.minus,
        TokenType.STAR: grammar.star,
        TokenType.DIV: grammar.div,
        TokenType.MOD: grammar.mod,
        TokenType.POT: grammar.pot,
        TokenType.POW2: grammar.pow2,

        # Boolean operators
        TokenType.AND: grammar.andp,
        TokenType.OR: grammar.or_,
        TokenType.NOT: grammar.not_,

        # Concat strings operators
        TokenType.CONCAT: grammar.concat,
        TokenType.CONCAT_SP: grammar.concat_sp,

        # Comparison operators
        TokenType.EQUAL_EQUAL: grammar.equal_equal,
        TokenType.NOT_EQUAL: grammar.not_equal,
        TokenType.LESS_EQUAL: grammar.less_equal,
        TokenType.GREATER_EQUAL: grammar.greater_equal,
        TokenType.LESS: grammar.less,
        TokenType.GREATER: grammar.greater,

        # Keywords
        TokenType.FUNC: grammar.func,
        TokenType.LET: grammar.let,
        TokenType.IN: grammar.in_,
        TokenType.IF: grammar.if_,
        TokenType.ELSE: grammar.else_,
        TokenType.ELIF: grammar.elif_,
        TokenType.WHILE: grammar.while_,
        TokenType.FOR: grammar.for_,
        TokenType.NEW: grammar.new,
        TokenType.IS: grammar.is_,
        TokenType.AS: grammar.as_,
        TokenType.PROTOCOL: grammar.protocol,
        TokenType.EXTENDS: grammar.extends,
        TokenType.TYPE: grammar.type_,
        TokenType.INHERITS: grammar.inherits,
        TokenType.BASE: grammar.base,
    }
        
    def __call__(self, tokens: List[Token]):
        #try:
        for token in tokens:
            token.token_type = self.tokens_terminals_map[token.token_type]
        derivation, operations, errors = super().__call__(tokens, True)
        return derivation, operations, errors
        #except : #ParserError as e:
            #error_token = tokens[e.token_index]
            #error_text = HulkSyntacticError.PARSING_ERROR % error_token.lex
            #errors = [HulkSyntacticError(error_text, error_token.row, error_token.column)]
        #    pass
        #    return None, None



