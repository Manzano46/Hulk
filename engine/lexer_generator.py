from cmp.automata import State
from engine.automaton import DFA
from engine.regex import Regex
from cmp.utils import Token

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            states = State.from_nfa(Regex(regex).automaton)
            for v in states:
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
            if new_state is not None and new_state[0] is not None:
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
        while len(text) > 0:            
            final, final_lex = self._walk(text)
            if len(final_lex) == 0 or final is None:
                raise 'error tokenize'
            print(final.tag)
            n, token_type = min(final.tag)
            text=text[len(final_lex):]
            yield final_lex, token_type
            
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]