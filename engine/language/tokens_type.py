from enum import Enum, auto

class TokenType(Enum):
    
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMI = auto()

    OPAR = auto()
    CPAR = auto()
    OPCUR = auto()
    CLCUR = auto()
    OPCOR = auto()
    CLCOR = auto()
    
    IDX = auto()
    STRING = auto()
    NUM = auto()
    BOOLEAN = auto()
    
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DIV = auto()
    MOD = auto()
    POT = auto()
    
    AND = auto()
    OR = auto()
    NOT = auto()

    CONCAT = auto()
    CONCAT_SP = auto()

    EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    
    FUNC = auto()
    LET = auto()
    IN = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    WHILE = auto()
    FOR = auto()
    NEW = auto()
    IS = auto()
    AS = auto()
    PROTOCOL = auto()
    EXTENDS = auto()
    TYPE = auto()
    INHERITS = auto()
    BASE = auto()

    ESCAPED_CHAR = auto()
    SPACES = auto()
    STRING_INF = auto()

    POW2 = auto()
    ARROW = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    DOUBLE_OR = auto()
    DESTRUCTIVE = auto()
    EOF = auto()
    
nonzero_digits = '|'.join(str(n) for n in range(1, 10))
digits = '|'.join(str(n) for n in range(10))
    
num = '|'.join([f"({nonzero_digits})({digits})*", f"({nonzero_digits})({digits})*.({digits})({digits})*", f"0.({digits})({digits})*", "0"])

lower_letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
upper_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))

identifier = f"(_|{upper_letters}|{lower_letters})(_|{upper_letters}|{lower_letters}|{digits})*"

key_words = [("let", TokenType.LET), ("in", TokenType.IN), ("if", TokenType.IF),("else", TokenType.ELSE), ("elif", TokenType.ELIF), ("function", TokenType.FUNC), ("while", TokenType.WHILE), ("for", TokenType.FOR), ("new", TokenType.NEW), ("is", TokenType.IS), ("as", TokenType.AS), ("protocol", TokenType.PROTOCOL), ("extends", TokenType.EXTENDS), ("type", TokenType.TYPE), ("inherits", TokenType.INHERITS), ("base", TokenType.BASE), ("true|false", TokenType.BOOLEAN)]

operators = [("{", TokenType.OPCUR), ("}", TokenType.CLCUR), (";", TokenType.SEMI), ("\\(", TokenType.OPAR), ("\\)", TokenType.CPAR), (",", TokenType.COMMA), ("=", TokenType.EQUAL), ("+", TokenType.PLUS), ("-", TokenType.MINUS), ("\\*", TokenType.STAR), ("/", TokenType.DIV), ("^", TokenType.POT), ("%", TokenType.MOD), ("<", TokenType.LESS), (">", TokenType.GREATER), ("&", TokenType.AND), ("\\|", TokenType.OR),("!", TokenType.NOT), ("@", TokenType.CONCAT), ("@@", TokenType.CONCAT_SP), (".", TokenType.DOT), (":", TokenType.COLON), ("\\[", TokenType.OPCOR), ("\\]", TokenType.CLCOR), ("\\*\\*", TokenType.POW2), ("=>", TokenType.ARROW), ("==", TokenType.EQUAL_EQUAL), ("!=", TokenType.NOT_EQUAL), (">=", TokenType.GREATER_EQUAL), ("<=", TokenType.LESS_EQUAL), ("\\|\\|", TokenType.DOUBLE_OR), (":=", TokenType.DESTRUCTIVE)]

string = "\"(\\\\\"|\\x00|\\x01|\\x02|\\x03|\\x04|\\x05|\\x06|\\x07|\\x08|\\t|\\n|\\x0b|\\x0c|\\r|\\x0e|\\x0f|\\x10|\\x11|\\x12|\\x13|\\x14|\\x15|\\x16|\\x17|\\x18|\\x19|\\x1a|\\x1b|\\x1c|\\x1d|\\x1e|\\x1f| |!|#|$|%|&|\'|\\(|\\)|\\*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|\\||}|~|\\x7f|\\x80|\\x81|\\x82|\\x83|\\x84|\\x85|\\x86|\\x87|\\x88|\\x89|\\x8a|\\x8b|\\x8c|\\x8d|\\x8e|\\x8f|\\x90|\\x91|\\x92|\\x93|\\x94|\\x95|\\x96|\\x97|\\x98|\\x99|\\x9a|\\x9b|\\x9c|\\x9d|\\x9e|\\x9f|\\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ|ÿ)*\""

string_inf = "\"(\\\\\"|\\x00|\\x01|\\x02|\\x03|\\x04|\\x05|\\x06|\\x07|\\x08|\\t|\\n|\\x0b|\\x0c|\\r|\\x0e|\\x0f|\\x10|\\x11|\\x12|\\x13|\\x14|\\x15|\\x16|\\x17|\\x18|\\x19|\\x1a|\\x1b|\\x1c|\\x1d|\\x1e|\\x1f| |!|#|$|%|&|\'|\\(|\\)|\\*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|\\||}|~|\\x7f|\\x80|\\x81|\\x82|\\x83|\\x84|\\x85|\\x86|\\x87|\\x88|\\x89|\\x8a|\\x8b|\\x8c|\\x8d|\\x8e|\\x8f|\\x90|\\x91|\\x92|\\x93|\\x94|\\x95|\\x96|\\x97|\\x98|\\x99|\\x9a|\\x9b|\\x9c|\\x9d|\\x9e|\\x9f|\\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ|ÿ)*"

hulk_tokens = operators + key_words + [(num, TokenType.NUM), (identifier, TokenType.IDX), (string, TokenType.STRING), (string_inf, TokenType.STRING_INF), ("  *", TokenType.SPACES), ("(\n|\t)(\n|\t)*", TokenType.ESCAPED_CHAR)]
#
hulk_tokens = [(x[1], x[0]) for x in hulk_tokens]
