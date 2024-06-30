
class Node:
    pass

# A program node has declaration and expression nodes
class ProgramNode(Node):
    def __init__(self, statements):
        self.statement = statements

class StatementNode(Node):
    pass
        
class DeclarationNode(StatementNode):
    pass
        
class ExpressionNode(StatementNode):
    pass

# A declaration node can be a function declaration, a type declaration or a protocol declaration
class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, expr, return_type=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.id = idx
        self.expr = expr
        self.return_type = return_type

class TypeDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, body, parent=None, parent_args=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else :
            self.params = []
            
        self.idx = idx
        self.methods = [method for method in body if isinstance(method, MethodDeclarationNode)]
        self.attributes = [attribute for attribute in body if isinstance(attribute, AttributeDeclarationNode)]
        self.parent = parent
        self.parent_args = parent_args

class ProtocolDeclarationNode(DeclarationNode):
    def __init__(self, idx, methods_signature, parent):
        super().__init__()
        self.idx = idx
        self.methods_signature = methods_signature
        self.parent = parent

# Other declarations
class VarDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr, var_type=None):
        super().__init__()
        self.id = idx
        self.expr = expr
        self.var_type = var_type


class MethodDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, expr, return_type=None):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.id = idx
        self.expr = expr
        self.return_type = return_type


class MethodSignatureDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type):
        super().__init__()
        if len(params) > 0:
            self.params = params
        else:
            self.params = []
        self.id = idx
        self.return_type = return_type

class AttributeDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr, attribute_type=None):
        super().__init__()
        self.id = idx
        self.expr = expr
        self.attribute_type = attribute_type

# An expression can be a special expression (let,if,while,for), a block expression or a simple expression
# Special expressions

class LetInNode(ExpressionNode):
    def __init__(self, var_declarations, expr):
        super().__init__()
        self.var_declarations = var_declarations
        self.expr = expr

class ConditionalNode(ExpressionNode):
    def __init__(self, condition_expression_list, else_expr):
        super().__init__()
        self.condition_expression_list = condition_expression_list
        self.else_expr = else_expr

class WhileNode(ExpressionNode):
    def __init__(self, condition, expression):
        super().__init__()
        self.condition = condition
        self.expression = expression

class ForNode(ExpressionNode):
    def __init__(self, var, iterable, expression):
        super().__init__()
        self.var = var
        self.iterable = iterable
        self.expression = expression

class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions

# Simple expressions
class DestructiveAssignmentNode(ExpressionNode):
    def __init__(self, var, expr):
        super().__init__()
        self.var = var
        self.expr = expr

class IsNode(ExpressionNode):
    def __init__(self, expression, ttype):
        super().__init__()
        self.expression = expression
        self.ttype = ttype


class AsNode(ExpressionNode):
    def __init__(self, expression, ttype):
        super().__init__()
        self.expression = expression
        self.ttype = ttype


class FunctionCallNode(ExpressionNode):
    def __init__(self, idx, args):
        super().__init__()
        self.idx = idx
        self.args = args

class IndexingNode(ExpressionNode):
    def __init__(self, obj, index):
        super().__init__()
        self.obj = obj
        self.index = index


class TypeInstantiationNode(ExpressionNode):
    def __init__(self, idx, args):
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
    def __init__(self, obj, method, args):
        super().__init__()
        self.obj = obj
        self.method = method
        self.args = args

class BaseCallNode(ExpressionNode):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.method_name = None
        self.parent_type = None



class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.operator = None


class UnaryExpressionNode(ExpressionNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = operand
        self.operator = None



class PrintNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

class AtomicNode(ExpressionNode):
    def __init__(self,lex):
        self.lex = lex
        

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

class VariableNode(AtomicNode):
    def __init__(self, lex, type):
        self.lex = lex
        self.type = type
    

        
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
