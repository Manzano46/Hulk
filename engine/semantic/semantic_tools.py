import cmp.visitor as visitor
from cmp.semantic import *
from engine.language.ast_nodes import *


def get_lca(*types: Type) -> Type:
    if not types or any(t.is_error() for t in types):
        return ErrorType()
    
    if any(t.is_unknow() for t in types):
        return UnknowType()
    
    lca = types[0]
    for typex in types[1:]:
        lca = _get_lca(lca, typex)

    return lca

def _get_lca(type1: Type, type2: Type) -> Type:
    # Object is the "root" of protocols too
    if type1 is None or type2 is None:
        return ObjectType()
    
    if type1.conforms_to(type2):
        return type2
    
    if type2.conforms_to(type1):
        return type1
    
    return _get_lca(type1.parent, type2.parent)

def get_lower_heir(var_name: str, *types: Type) -> Type:
    if not types or any(isinstance(t, ErrorType) for t in types):
        return ErrorType()
    
    if any(t.is_unknow() for t in types):
        return UnknowType()
    
    heir = types[0]
    for typex in types[1:]:
        if typex.conforms_to(heir):
            heir = typex

        elif not heir.conforms_to(typex):
            raise SemanticError(SemanticError.INCONSISTENT_USE % var_name)
        
    return heir