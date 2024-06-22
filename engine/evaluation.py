from cmp.pycompiler import Symbol, NonTerminal, Terminal, EOF, Sentence, Epsilon, Production, Grammar
from cmp.utils import Token

def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return
    
    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)
    
    assert isinstance(next(tokens).token_type, EOF)
    return result
    

def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes
    
    synteticed = [None] * len(attributes)
    inherited = [None] * len(attributes)
    inherited[0] = inherited_value
    

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            token = next(tokens)
            try:
                synteticed[i] = float(token.lex)
            except:
                raise 'cannot convert to float'
            
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            
            if attributes[i] is not None:
                inherited[i] = attributes[i](inherited, synteticed)
            
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])
    
    return attributes[0](inherited, synteticed)
