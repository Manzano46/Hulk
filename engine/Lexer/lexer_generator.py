from engine.Lexer.regex import Regex
from cmp.automata import State
from cmp.utils import Token
# import pydot
from engine.language.errors import * #HulkLexicographicError
# from engine.automaton.automaton import NFA, DFA, nfa_to_dfa
# from engine.automaton.automaton_operations import automata_union, automata_concatenation, automata_closure, automata_minimization
class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            #print(n, token_type, regex)
            states = State.from_nfa(Regex(regex).automaton())
            for v in states:
                #print(v)
                if v.final:  
                    v.tag = (n, token_type)
            regexs.append(states)
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        for v in self.regexs:
            start.add_epsilon_transition(v)
        return start.to_deterministic()
    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        for symbol in string:
            new_state = state[symbol]
            if new_state is not None:
                new_state = new_state[0]
                lex += symbol
                
                if new_state.final:
                    if new_state.tag is None:
                        new_state.tag = list(map(lambda x:x.tag, filter(lambda x:x.tag is not None, new_state.state)))
                    final = new_state
                    final_lex = lex
                state = new_state
            else:
                break
            
        return final, final_lex
    
    def _tokenize(self, text):
        row = 0
        column = 0
        

        while len(text) > 0:
            final, final_lex = self._walk(text)
            if len(final_lex) == 0 or final is None:
                raise HulkLexicographicError(HulkLexicographicError.INVALID_CARATER % (row, column), row, column)

            n, token_type = min(final.tag)
            
            yield final_lex, token_type, row, column
            
            splited = final_lex.split('\n')
            
            if len(splited) > 1:
                row += len(splited) - 1
                column = 0            
            column += len(splited[-1])
            
            text=text[len(final_lex):]
            
        yield '$', self.eof, row, column
    
    def __call__(self, text):
        return [ Token(lex, ttype, row, column) for lex, ttype, row, column in self._tokenize(text) ]