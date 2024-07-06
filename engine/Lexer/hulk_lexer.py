from engine.lexer.lexer_generator import Lexer
from engine.language.tokens_type import *
from engine.language.errors import * #HulkLexicographicError

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
                raise HulkLexicographicError(HulkLexicographicError.STRING_INF % (tk.row, tk.column),tk.row, tk.column)
        return filtered_tokens