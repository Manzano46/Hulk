from engine.automaton import NFA, DFA, nfa_to_dfa
from cmp.utils import DisjointSet

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[origin + d1, symbol] = [dest + d1 for dest in destinations]
        
    for (origin, symbol), destinations in a2.map.items():        
        transitions[origin + d2, symbol] = [dest + d2 for dest in destinations]

    trans = transitions.get((start, ''), [])
    transitions[start, ''] = trans + [d1, d2]
    
    for f1 in a1.finals:
        trans = transitions.get((f1 + d1, ''), [])
        transitions[f1 + d1, ''] = trans + [final]
    for f2 in a2.finals:
        trans = transitions.get((f2 + d2, ''), [])
        transitions[f2 + d2, ''] = trans + [final]
            
    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)


def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        new_origin = origin + d1 
        new_destinations = [x + d1 for x in destinations]
        
        transitions[(new_origin,symbol)] = new_destinations
        

    for (origin, symbol), destinations in a2.map.items():
        new_origin = origin + d2 
        new_destinations = [x + d2 for x in destinations]
        
        transitions[(new_origin,symbol)] = new_destinations
            
    for state in a1.finals:
        new_state = state + d1
        if (new_state, '') not in transitions:
            transitions[(new_state,'')] = [] 
        transitions[(new_state , '')].extend([d2])
    
    for state in a2.finals:
        new_state = state + d2
        if (new_state, '') not in transitions:
            transitions[(new_state,'')] = [] 
        transitions[(new_state , '')].extend([final])   
            
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        new_origin = origin + d1
        new_destinations = [v + d1 for v in destinations]
        
        transitions[(new_origin, symbol)] = new_destinations
    
    transitions[(start, '')] = [d1, final]

    for state in a1.finals:
        new_state = state + d1
        if (new_state, '') not in transitions:
            transitions[(new_state,'')] = [] 
        transitions[(new_state , '')].extend([final])
        
    
    if (final, '') not in transitions:
        transitions[(final,'')] = [] 
    transitions[(final,'')].extend([start])
            
    states = a1.states +  2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        key = []
        member = member.value
        for symbol in vocabulary:
            
            if symbol in automaton.transitions[member]:
                parent = partition[automaton.transitions[member][symbol][0]].representative
            else:
                parent = -1
            key.append(parent)
        key = tuple(key)
        if key not in split:
            split[key] = []
        split[key].append(member)

    return [ group for group in split.values()]
            
def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    partition.merge(automaton.finals)
    no_finals = [x for x in range(automaton.states) if x not in automaton.finals]
    partition.merge(no_finals)
    
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        
        for group in partition.groups:
            for subgroup in distinguish_states(group, automaton, partition):
                new_partition.merge(subgroup)

        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automata_minimization(automaton):
    partition = state_minimization(automaton)
    
    states = [s for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):

        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():
            destination = partition[destinations[0]].representative
            
            try:
                transitions[(i,symbol)]
                assert False
            except KeyError:
                transitions[(i, symbol)] = states.index(destination)

    finals = [states.index(partition[x].representative) for x in automaton.finals]
    start = states.index(partition[automaton.start].representative)
    
    return DFA(len(states), finals, transitions, start)