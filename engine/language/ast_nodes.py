from abc import ABC
from cmp.semantic import *


class Node(ABC):
    def __init__(self):
        self.scope = None

# A program node has declaration and expression nodes
class ProgramNode(Node):
    def __init__(self, declarations, global_expression):
        super().__init__()
        self.declarations = declarations
        self.expression = global_expression

        
class DeclarationNode(Node,ABC):
    pass
        
class ExpressionNode(Node,ABC):
    pass

class AtomicNode(ExpressionNode):
    def __init__(self,lex):
        self.lex = lex
        
class VariableNode(AtomicNode):
    def __init__(self, lex, type=None):
        super().__init__(lex)
        self.type: Type = type
    
# A declaration node can be a function declaration, a type declaration or a protocol declaration
class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, params:list[VariableNode], expr:ExpressionNode, return_type: Type=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.id = idx
        self.expr: ExpressionNode = expr
        self.return_type = return_type

class MethodDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, params:list[VariableNode], expr:ExpressionNode, return_type=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.name = idx
        self.expr: ExpressionNode = expr
        self.return_type: Type = return_type


class MethodSignatureDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, params:list[VariableNode], return_type):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.name = idx
        self.return_type: Type = return_type

class AttributeDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, expr:ExpressionNode, attribute_type=None):
        super().__init__()
        self.name = idx
        self.expr: ExpressionNode = expr
        self.attribute_type: Type = attribute_type

class TypeDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, params:list[VariableNode], body, parent=None, parent_args=[]):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else :
            self.params = []
            
        self.name = idx
        self.methods = {(method.name,method) for method in body if isinstance(method, MethodDeclarationNode)}
        self.attributes = {(attribute.name,attribute) for attribute in body if isinstance(attribute, AttributeDeclarationNode)}
        self.parent: TypeDeclarationNode = parent
        self.parent_args = parent_args


class ProtocolDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, methods_signature:list[MethodSignatureDeclarationNode], parent):
        super().__init__()
        self.idx = idx
        self.methods_signature = methods_signature
        self.parent = parent

# Other declarations
class VarDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, expr:ExpressionNode, var_type=None):
        super().__init__()
        self.id = idx
        self.expr: ExpressionNode = expr
        self.var_type: Type = var_type



# An expression can be a special expression (let,if,while,for), a block expression or a simple expression
# Special expressions

class LetInNode(ExpressionNode):
    def __init__(self, var_declarations:list[VarDeclarationNode], expr:ExpressionNode):
        super().__init__()
        self.var_declarations = var_declarations
        self.expr = expr

class ConditionalNode(ExpressionNode):
    def __init__(self, condition_expression_list: list[tuple], else_expr:ExpressionNode):
        super().__init__()
        self.condition_expression_list = condition_expression_list
        self.else_expr = else_expr

class WhileNode(ExpressionNode):
    def __init__(self, condition, expression:ExpressionNode):
        super().__init__()
        self.condition = condition
        self.expression = expression

class ForNode(ExpressionNode):
    def __init__(self, var, iterable, expression:ExpressionNode):
        super().__init__()
        self.var = var
        self.iterable = iterable
        self.expression = expression

class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expressions:list[ExpressionNode]):
        super().__init__()
        self.expressions = expressions

# Simple expressions
class DestructiveAssignmentNode(ExpressionNode):
    def __init__(self, var, expr:ExpressionNode):
        super().__init__()
        self.var = var
        self.expr = expr

class IsNode(ExpressionNode):
    def __init__(self, expression:ExpressionNode, ttype):
        super().__init__()
        self.expression = expression
        self.ttype = ttype


class AsNode(ExpressionNode):
    def __init__(self, expression:ExpressionNode, ttype):
        super().__init__()
        self.expression = expression
        self.ttype = ttype


class FunctionCallNode(ExpressionNode):
    def __init__(self, idx:str, args:list[ExpressionNode]):
        super().__init__()
        self.idx = idx
        self.args = args

class IndexingNode(ExpressionNode):
    def __init__(self, obj, index):
        super().__init__()
        self.obj = obj
        self.index = index


class TypeInstantiationNode(ExpressionNode):
    def __init__(self, idx, args:list[ExpressionNode]):
        super().__init__()
        self.idx = idx
        self.args = args

class AttributeCallNode(ExpressionNode):
    def __init__(self, obj, attribute):
        super().__init__()
        self.obj = obj
        self.attribute = attribute

class VectorInitializationNode(ExpressionNode):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

class VectorComprehensionNode(ExpressionNode):
    def __init__(self, selector, var, iterable):
        super().__init__()
        self.selector = selector
        self.var = var
        self.iterable = iterable

class MethodCallNode(ExpressionNode):
    def __init__(self, obj, method, args:list[ExpressionNode]):
        super().__init__()
        self.obj = obj
        self.method = method
        self.args = args

class BaseCallNode(ExpressionNode):
    def __init__(self, args:list[ExpressionNode]):
        super().__init__()
        self.args = args
        self.method_name = None
        self.parent_type = None



class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode):
        super().__init__()
        self.left = left
        self.right = right
        self.operator = None


class UnaryExpressionNode(ExpressionNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = operand
        self.operator = None



class NumberNode(AtomicNode):
    #def __init__(self,lex):
        #self.lex = float(lex)
    pass

class StringNode(AtomicNode):
    #def __init__(self, lex):
        #self.lex = str(lex)
    pass

class BooleanNode(AtomicNode):
    #def __init__(self, lex):
        #self.lex = bool(lex)
    pass

        
class StrBinaryExpressionNode(BinaryExpressionNode):
    pass


class BoolBinaryExpressionNode(BinaryExpressionNode):
    pass


class InequalityExpressionNode(BinaryExpressionNode):
    pass


class ArithmeticExpressionNode(BinaryExpressionNode):
    pass


class EqualityExpressionNode(BinaryExpressionNode):
    pass


class NotNode(UnaryExpressionNode):
    pass


class NegNode(UnaryExpressionNode):
    pass



class ConcatNode(StrBinaryExpressionNode):
    def __init__(self, left, right,operator):
        super().__init__(left, right)
        self.operator = operator


class OrNode(BoolBinaryExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '|'


class AndNode(BoolBinaryExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '&'


class LessThanNode(InequalityExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '<'


class GreaterThanNode(InequalityExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '>'


class LessOrEqualNode(InequalityExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '<='


class GreaterOrEqualNode(InequalityExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '>='


class PlusNode(ArithmeticExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '+'


class MinusNode(ArithmeticExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '-'


class StarNode(ArithmeticExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '*'


class DivNode(ArithmeticExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '/'


class ModNode(ArithmeticExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '%'


class PowNode(ArithmeticExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
      


class EqualNode(EqualityExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '=='


class NotEqualNode(EqualityExpressionNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.operator = '!='
