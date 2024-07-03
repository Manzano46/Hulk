from typing import List
from engine.language.ast_nodes import *
import cmp.visitor as visitor
from cmp.semantic import *
from semantic.semantic_tools import *


class TypeChecker(object):
    def __init__(self, context, errors=None):
        if errors is None:
            errors = []
        self.context: Context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node: Node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.expression)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode):
        self.current_type = self.context.get_type(node.name)

        if self.current_type.is_error():
            return

        for attr in node.attributes:
            self.visit(attr)

        for method in node.methods:
            self.visit(method)

        if self.current_type.parent.is_error():
            return
        # recojo los tipos de argumento que estoy pasando a mi padre
        parent_args_types = [self.visit(expr) for expr in node.parent_args]
        # recojo los tipos de los paramentros de mi padre
        parent_params_types = self.current_type.parent.params_type
        # si la cantidad de argumentos de mi padre no es la misma que la cantidad de parametros que recibe
        if len(parent_args_types) != len(parent_params_types):
            error_text = SemanticError.EXPECTED_ARGUMENTS % (
                len(parent_params_types), len(parent_args_types), self.current_type.parent.name)
            self.errors.append(SemanticError(error_text))
            return ErrorType()

        for parent_arg_type, parent_param_type in zip(parent_args_types, parent_params_types):
            if not parent_arg_type.conforms_to(parent_param_type):
                error_text = SemanticError.INCOMPATIBLE_TYPES % (parent_arg_type.name, parent_param_type.name)
                self.errors.append(SemanticError(error_text))

        self.current_type = None

    @visitor.when(AttributeDeclarationNode)
    def visit(self, node: AttributeDeclarationNode):
        infered_type = self.visit(node.expr)

        attr_type = self.current_type.get_attribute(node.name).type

        if not infered_type.conforms_to(attr_type):
            error_text = SemanticError.INCOMPATIBLE_TYPES % (infered_type.name, attr_type.name)
            self.errors.append(SemanticError(error_text))

        return attr_type

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode):
        self.current_method = self.current_type.get_method(node.name)

        infered_type = self.visit(node.expr)

        if not infered_type.conforms_to(self.current_method.return_type):
            error_text = SemanticError.INCOMPATIBLE_TYPES % (infered_type.name, self.current_method.return_type.name)
            self.errors.append(SemanticError(error_text))

        return_type = self.current_method.return_type

        # Check if override is correct
        if self.current_type.parent is None or self.current_type.parent.is_error():
            return return_type

        try:
            parent_method = self.current_type.parent.get_method(node.name)
        except SemanticError:
            return return_type

        error_text = SemanticError.WRONG_SIGNATURE % self.current_method.name

        if parent_method.return_type != return_type:
            self.errors.append(SemanticError(error_text))
        elif len(parent_method.param_types) != len(self.current_method.param_types):
            self.errors.append(SemanticError(error_text))
        else:
            for i, parent_param_type in enumerate(parent_method.param_types):
                param_type = self.current_method.param_types[i]
                if parent_param_type != param_type:
                    self.errors.append(SemanticError(error_text))

        self.current_method = None

        return return_type

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        function: Method = self.context.get_function(node.id)

        infered_return_type = self.visit(node.expr)

        if not infered_return_type.conforms_to(function.return_type):
            error_text = SemanticError.INCOMPATIBLE_TYPES % (infered_return_type.name, function.return_type.name)
            self.errors.append(SemanticError(error_text))
            return ErrorType()

        return function.return_type

    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode):
        expr_type = ErrorType()

        for expr in node.expressions:
            expr_type = self.visit(expr)
        return expr_type

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode):
        scope = node.scope

        infered_type = self.visit(node.expr)
        var_type = scope.find_variable(node.id).type

        if not infered_type.conforms_to(var_type):
            error_text = SemanticError.INCOMPATIBLE_TYPES % (infered_type.name, var_type.name)
            self.errors.append(SemanticError(error_text))
            var_type = ErrorType()

        return var_type

    @visitor.when(LetInNode)
    def visit(self, node: LetInNode):

        for declaration in node.var_declarations:
            self.visit(declaration)

        return self.visit(node.expr)

    @visitor.when(DestructiveAssignmentNode)
    def visit(self, node: DestructiveAssignmentNode):
        new_type = self.visit(node.expr)
        old_type = self.visit(node.var)

        if old_type.name == 'Self':
            self.errors.append(SemanticError(SemanticError.SELF_IS_READONLY))
            return ErrorType()

        if not new_type.conforms_to(old_type):
            error_text = SemanticError.INCOMPATIBLE_TYPES % (new_type.name, old_type.name)
            self.errors.append(SemanticError(error_text))
            return ErrorType()

        return old_type

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode):
        cond_types = [self.visit(cond[0]) for cond in node.condition_expression_list]

        for cond_type in cond_types:
            if cond_type != BooleanType():
                error_text = SemanticError.INCOMPATIBLE_TYPES % (cond_type.name, BooleanType().name)
                self.errors.append(SemanticError(error_text))

        expr_types = [self.visit(expression[1]) for expression in node.condition_expression_list]

        else_type = self.visit(node.else_expr)

        return get_lowest_common_ancestor(expr_types + [else_type])

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        cond_type = self.visit(node.condition)

        if cond_type != BooleanType():
            error_text = SemanticError.INCOMPATIBLE_TYPES % (cond_type.name, BooleanType().name)
            self.errors.append(SemanticError(error_text))

        return self.visit(node.expression)

    @visitor.when(ForNode)
    def visit(self, node: ForNode):
        ttype = self.visit(node.iterable)
        iterable_protocol = self.context.get_protocol('Iterable')

        if not ttype.conforms_to(iterable_protocol):
            error_text = SemanticError.INCOMPATIBLE_TYPES % (ttype.name, iterable_protocol.name)
            self.errors.append(SemanticError(error_text))

        return self.visit(node.expression)

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode):
        args_types = [self.visit(arg) for arg in node.args]

        try:
            function = self.context.get_function(node.idx)
        except SemanticError as e:
            self.errors.append(e)
            for arg in node.args:
                self.visit(arg)
            return ErrorType()

        if len(args_types) != len(function.param_types):
            error_text = SemanticError.EXPECTED_ARGUMENTS % (
                len(function.param_types), len(args_types), function.name)
            self.errors.append(SemanticError(error_text))
            return ErrorType()

        for arg_type, param_type in zip(args_types, function.param_types):
            if not arg_type.conforms_to(param_type):
                error_text = SemanticError.INCOMPATIBLE_TYPES % (arg_type.name, param_type.name)
                self.errors.append(SemanticError(error_text))
                return ErrorType()

        return function.return_type

    