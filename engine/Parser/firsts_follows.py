from cmp.utils import ContainerSet

def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    
    
    if alpha_is_epsilon:
        first_alpha.set_epsilon(True)
    
    elif alpha[0].IsTerminal:
        first_alpha.add(alpha[0])
    else:
        Y = alpha[0]
        
        if len(alpha) > 1:
            first_alpha.update(firsts[Y])
        else:
            first_alpha.hard_update(firsts[Y])
        
        if len(alpha) > 1:
            Z = alpha[1:]
            if firsts[Y].contains_epsilon:
                first_alpha.hard_update(compute_local_first(firsts,Z))
    
    return first_alpha

def compute_firsts(G):
    firsts = {}
    change = True
    
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            first_X = firsts[X]
                
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            local_first = compute_local_first(firsts, alpha)
            
            
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    return firsts


from itertools import islice

def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            for i in range(0, len(alpha)):
                A = alpha[i]    
                    
                if A.IsNonTerminal:
                    firsts_Z = ContainerSet()
                    if i + 1 < len(alpha):
                        firsts_Z = compute_local_first(firsts, alpha[i+1:])  
                                          
                    change = change or follows[A].update(firsts_Z)
                    
                    if firsts_Z.contains_epsilon or i == len(alpha)-1:
                        change = change or follows[A].update(follow_X)

    return follows

def compute_firsts_follows(G):
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
    return firsts, follows