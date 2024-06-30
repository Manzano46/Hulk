from engine.lexer_generator import Lexer
from engine.tokens_type import *

class HulkLexer(Lexer):
    def __init__(self, table, eof):
        
        super().__init__(table, eof)
    
    def __call__(self, text):
        tokens = super().__call__(text)
        
        filtered_tokens = [token for token in tokens if token.is_valid and
                           token.token_type not in [TokenType.SPACES, TokenType.ESCAPED_CHAR,
                                                    TokenType.STRING_INF]]
        for tk in tokens:
            if tk.token_type == TokenType.STRING_INF:
                raise "string sin completar"
        return filtered_tokens