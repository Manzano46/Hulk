import cmp.visitor as visitor
from cmp.semantic import SemanticError, Context, ErrorType, Scope
from engine.language.ast_nodes import *

class VarCollector:
    def __init__(self, context: Context, errors = []):
        self.context = context
        self.errors = errors
        self.current_type = None

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope = None):
        scope = Scope()
        node.scope = scope

        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())

        self.visit(node.expression, scope.create_child())
        return scope
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node, scope):
        node.scope = scope

        self.current_type = self.context.get_type(node.name)
        if self.current_type.is_error():
            return
        
        for param in node.params:
            if param.type == None:
                scope.define_variable(param.lex, UnknowType())
            else:
                scope.define_variable(param.lex, param.type)

        scope.define_variable('self', self.current_type)

        for attribute in node.attributes:
            self.visit(attribute, scope.create_child())
            
        for method in node.methods:
            self.visit(method, scope.create_chid())

    @visitor.when(AttributeDeclarationNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scope):
        node.scope = scope

        method = self.current_type.get_method(node.name)
        for i, param_name in enumerate(method.param_names):
            param_type = method.param_types[i]
            scope.define_variable(param_name, param_type)

        self.visit(node.expr, scope.create_child())

    @visitor.when(ExpressionBlockNode)
    def visit(self, node, scope):
        node.scope = scope
        
        for expr in node.expressions:
            self.visit(expr, scope.create_child())
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

        var_type = None
        if node.var_type is not None:
            try:
                var_type = self.context.get_type_or_protocol(node.var_type)
            except SemanticError as e:
                self.errors.append(e)
                var_type = ErrorType()
        
        scope.define_variable(node.id, var_type)


    @visitor.when(LetInNode)
    def visit(self, node, scope):
        node.scope = scope
        for declaration in node.declarations:
            self.visit(declaration, scope)

        self.visit(node.body, scope.create_child())

    @visitor.when(DestructiveAssignmentNode)
    def visit(self, node: DestructiveAssignmentNode, scope: Scope):
        node.scope = scope
        self.visit(node.target, scope.create_child())
        self.visit(node.expr, scope.create_child())

    @visitor.when(BinaryExpressionNode)
    def visit(self, node: BinaryExpressionNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(UnaryExpressionNode)
    def visit(self, node: UnaryExpressionNode, scope: Scope):
        node.scope = scope
        self.visit(node.operand, scope.create_child())

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        node.scope = scope
        for condition in node.conditions:
            self.visit(condition, scope.create_child())

        for expression in node.expressions:
            self.visit(expression, scope.create_child())

        self.visit(node.default_expr, scope.create_child())

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        node.scope = scope
        self.visit(node.condition, scope.create_child())
        self.visit(node.expression, scope.create_child())

    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        node.scope = scope
        expr_scope = scope.create_child()

        expr_scope.define_variable(node.var, UnknowType(), is_parameter=True)

        self.visit(node.iterable, scope.create_child())
        self.visit(node.expression, expr_scope)

    @visitor.when(IsNode)
    def visit(self, node: IsNode, scope: Scope):
        node.scope = scope
        self.visit(node.expression, scope.create_child())

    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        node.scope = scope
        self.visit(node.expression, scope.create_child())

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope: Scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode, scope: Scope):
        node.scope = scope
        self.visit(node.obj, scope.create_child())

    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope: Scope):
        node.scope = scope
        self.visit(node.obj, scope.create_child())
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(TypeInstantiationNode)
    def visit(self, node: TypeInstantiationNode, scope: Scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(VectorInitializationNode)
    def visit(self, node: VectorInitializationNode, scope: Scope):
        node.scope = scope
        for element in node.elements:
            self.visit(element, scope.create_child())

    @visitor.when(VectorComprehensionNode)
    def visit(self, node: VectorComprehensionNode, scope: Scope):
        node.scope = scope

        selector_scope = scope.create_child()
        selector_scope.define_variable(node.var, UnknowType(), is_parameter=True)
        self.visit(node.selector, selector_scope)

        self.visit(node.iterable, scope.create_child())

    @visitor.when(IndexingNode)
    def visit(self, node: IndexingNode, scope: Scope):
        node.scope = scope

        self.visit(node.obj, scope.create_child())
        self.visit(node.index, scope.create_child())

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        node.scope = scope

    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope):
        node.scope = scope

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope: Scope):
        node.scope = scope

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        node.scope = scope

        
    

