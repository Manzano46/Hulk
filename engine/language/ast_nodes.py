from abc import ABC
from cmp.semantic import *


class Node(ABC):
    def __init__(self):
        self.scope: Scope

# A program node has declaration and expression nodes
class ProgramNode(Node):
    def __init__(self, declarations, global_expression):
        super().__init__()
        self.declarations = declarations
        self.expression = global_expression

        
class DeclarationNode(Node):
    pass
        
class ExpressionNode(Node):
    pass

class AtomicNode(ExpressionNode, ABC):
    def __init__(self,token):
        super().__init__()
        self.lex = token.lex
        
class VariableNode(AtomicNode):
    def __init__(self, token, token_type=None):
        self.lex = token.lex
        self.type = token_type.lex if token_type != None else None 
        self.row = token.row
        self.column = token.column
    
# A declaration node can be a function declaration, a type declaration or a protocol declaration
class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, token, params:list[VariableNode], expr:ExpressionNode, token_return_type=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.id = token.lex
        self.expr: ExpressionNode = expr
        self.return_type = token_return_type.lex if token_return_type != None else None
        self.row = token.row
        self.column = token.column

class MethodDeclarationNode(DeclarationNode):
    def __init__(self, token, params:list[VariableNode], expr:ExpressionNode, token_return_type=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.name = token.lex
        self.expr: ExpressionNode = expr
        self.return_type = token_return_type.lex if token_return_type != None else None
        self.row = token.row
        self.column = token.column


class MethodSignatureDeclarationNode(DeclarationNode):
    def __init__(self, token, params:list[VariableNode], token_return_type=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.name = token.lex
        self.return_type = token_return_type.lex if token_return_type != None else None
        self.row = token.row
        self.column = token.column

class AttributeDeclarationNode(DeclarationNode):
    def __init__(self, token, expr:ExpressionNode, token_attribute_type=None):
        super().__init__()
        self.name = token.lex
        self.expr: ExpressionNode = expr
        self.attribute_type = token_attribute_type.lex if token_attribute_type != None else None
        self.row = token.row
        self.column = token.column

class TypeDeclarationNode(DeclarationNode):
    def __init__(self, token, params:list[VariableNode], body, token_parent=None, parent_args=[]):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else :
            self.params = []
            
        self.name = token.lex
        self.methods = {(method.name,method) for method in body if isinstance(method, MethodDeclarationNode)}
        self.attributes = {(attribute.name,attribute) for attribute in body if isinstance(attribute, AttributeDeclarationNode)}
        self.parent = token_parent.lex if token_parent != None else None
        self.parent_args = parent_args
        self.row = token.row
        self.column = token.column


class ProtocolDeclarationNode(DeclarationNode):
    def __init__(self, token, methods_signature:list[MethodSignatureDeclarationNode], parent):
        super().__init__()
        self.idx = token.lex
        self.methods_signature = methods_signature
        self.parent = parent
        self.row = token.row
        self.column = token.column

# Other declarations
class VarDeclarationNode(DeclarationNode):
    def __init__(self, token, expr:ExpressionNode, token_var_type=None):
        super().__init__()
        self.id = token.lex
        self.expr: ExpressionNode = expr
        self.var_type = token_var_type.lex if token_var_type != None else None
        self.row = token.row
        self.column = token.column



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
    def __init__(self, condition, expression:ExpressionNode, token):
        super().__init__()
        self.condition = condition
        self.expression = expression
        self.row = token.row
        self.column = token.column

class ForNode(ExpressionNode):
    def __init__(self, var, iterable, expression:ExpressionNode, token):
        super().__init__()
        self.var = var
        self.iterable = iterable
        self.expression = expression
        self.row = token.row
        self.column = token.column

class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expressions:list[ExpressionNode]):
        super().__init__()
        self.expressions = expressions

# Simple expressions
class DestructiveAssignmentNode(ExpressionNode):
    def __init__(self, var, expr:ExpressionNode, token):
        super().__init__()
        self.var = var
        self.expr = expr
        self.row = token.row
        self.column = token.column
        

class IsNode(ExpressionNode):
    def __init__(self, expression:ExpressionNode, ttype):
        super().__init__()
        self.expression = expression
        self.ttype = ttype.lex
        self.row = ttype.row
        self.column = ttype.column


class AsNode(ExpressionNode):
    def __init__(self, expression:ExpressionNode, ttype):
        super().__init__()
        self.expression = expression
        self.ttype = ttype.lex
        self.row = ttype.row
        self.column = ttype.column


class FunctionCallNode(ExpressionNode):
    def __init__(self, token, args:list[ExpressionNode]):
        super().__init__()
        self.idx = token.lex
        self.args = args
        self.row = token.row
        self.column = token.column

class IndexingNode(ExpressionNode):
    def __init__(self, obj, index):
        super().__init__()
        self.obj = obj
        self.index = index


class TypeInstantiationNode(ExpressionNode):
    def __init__(self, token, args:list[ExpressionNode]):
        super().__init__()
        self.idx = token.lex
        self.args = args
        self.row = token.row
        self.column = token.column

class AttributeCallNode(ExpressionNode):
    def __init__(self, obj, token_attribute):
        super().__init__()
        self.obj = obj
        self.attribute = token_attribute.lex
        self.row = token_attribute.row
        self.column = token_attribute.column

class VectorInitializationNode(ExpressionNode):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

class VectorComprehensionNode(ExpressionNode):
    def __init__(self, selector, token_var, iterable):
        super().__init__()
        self.selector = selector
        self.var = token_var.lex
        self.iterable = iterable
        self.row = token_var.row
        self.column = token_var.column

class MethodCallNode(ExpressionNode):
    def __init__(self, obj, token_method, args:list[ExpressionNode]):
        super().__init__()
        self.obj = obj
        self.method = token_method.lex
        self.args = args
        self.row = token_method.row
        self.column = token_method.column

class BaseCallNode(ExpressionNode):
    def __init__(self, token, args:list[ExpressionNode]):
        super().__init__()
        self.args = args
        self.method_name = None
        self.parent_type = None
        self.row = token.row
        self.column = token.column



class BinaryExpressionNode(ExpressionNode, ABC):
    def __init__(self, left:ExpressionNode, right:ExpressionNode):
        super().__init__()
        self.left = left
        self.right = right
        self.operator = None


class UnaryExpressionNode(ExpressionNode, ABC):
    def __init__(self, operand):
        super().__init__()
        self.operand = operand
        self.operator = None


class NumberNode(AtomicNode):
    def __init__(self,token):
        self.lex = token.lex
        self.row = token.row
        self.column = token.column
    

class StringNode(AtomicNode):
    def __init__(self,token):
        self.lex = token.lex
        self.row = token.row
        self.column = token.column

class BooleanNode(AtomicNode):
    def __init__(self,token):
        self.lex = token.lex
        self.row = token.row
        self.column = token.column

        
class StrBinaryExpressionNode(BinaryExpressionNode, ABC):
    pass


class BoolBinaryExpressionNode(BinaryExpressionNode, ABC):
    pass


class InequalityExpressionNode(BinaryExpressionNode, ABC):
    pass


class ArithmeticExpressionNode(BinaryExpressionNode, ABC):
    pass


class EqualityExpressionNode(BinaryExpressionNode, ABC):
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
