import cmp.visitor as visitor
from cmp.semantic import *
from engine.language.ast_nodes import *
from semantic_tools import get_lca

class TypeInferer(object):
    def __init__(self, context, errors=[]):
        self.errors = errors
        self.context = context


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.expression)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        self.current_type: Type = self.context.get_type(node.name)

        if self.current_type.is_error():
            return
        
        parent_args_types = [self.visit(arg) for arg in node.parent_args]
        if not self.current_type.parent.is_error():
            for arg, arg_type in zip(node.parent_args, self.current_type.parent.params_type):
                self.pass_type(arg, arg.scope, arg_type)

            for i, param_type in enumerate(self.current_type.parent.params_types):
                if len(parent_args_types) <= i:
                        break
                
                arg = parent_args_types[i]
                if param_type.is_unknow() and not param_type.is_error():
                    var = self.current_type.parent.param_vars[i]
                    var.inferred_types.append(arg)

        for attribute in node.attributes:
            self.visit(attribute)


        for i, param_type in enumerate(self.current_type.params_types):
            param_name = self.current_type.params_names[i]
            local_var = node.scope.find_variable(param_name)
            local_var.type = param_type
            # Check if we could infer the param type in the body
            if param_type.is_unknown and local_var.is_param and local_var.inferred_types:
                try:
                    new_type = types.get_most_specialized_type(local_var.inferred_types, var_name=param_name)
                except SemanticError as e:
                    self.errors.append(e)
                    new_type = ErrorType()
                self.current_type.params_types[i] = new_type
                if not isinstance(new_type, types.AutoType):
                    self.had_changed = True
                local_var.set_type_and_clear_inference_types_list(new_type)
            # Check if we could infer the param type in a call
            if (self.current_type.params_types[i].is_unknown() and self.current_type.param_vars[i].inferred_types):
                new_type = get_lca(self.current_type.param_vars[i].inferred_types)
                self.current_type.params_types[i] = new_type
                if not new_type.is_unknow():
                    # self.had_changed = True
                    pass
                local_var.set_type_and_clear_inference_types_list(new_type)

            # Infer the params types and return type of the methods
        for method in node.methods:
            self.visit(method)

        self.current_type = None

    @visitor.when(AttributeDeclarationNode)
    def visit(self, node):
        inf_type = self.visit(node.expr)

        attribute: Attribute = self.current_type.get_attribute(node.name)

        if attribute.type.is_error():
            attr_type = ErrorType()

        elif not attribute.type.is_unknow():
            attr_type = attribute.type

        else:
            attr_type = inf_type

        attribute.type = attr_type
        return attr_type
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node):
        # Incompleto
        raise NotImplementedError()
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node):
        expr_type = ErrorType()
        for expr in node.expressions:
            expr_type = self.visit(expr)
        return expr_type
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node):
        inf_type = self.visit(node.expr)
        var = node.scope.find_variable(node.id)
        var.type = var.type if not var.type.is_unknow() or var.type.is_error() else inf_type
        return var.type

    @visitor.when(LetInNode)
    def visit(self, node):
        for declaration in node.var_declarations:
            self.visit(declaration)
        return self.visit(node.body)
    
    @visitor.when(DestructiveAssignmentNode)
    def visit(self, node):
        new_type = self.visit(node.expr)
        old_type = self.visit(node.target)

        if old_type.name == 'Self':
            return ErrorType()

        if new_type.is_unknow() and not old_type.is_unknow():
            self.pass_type(node.expr, node.scope, old_type)

        return old_type
    
    @visitor.when(ConditionalNode)
    def visit(self, node):
        for cond in node.conditions:
            self.visit(cond)

        expr_types = [self.visit(expression) for expression in node.expressions]

        else_type = self.visit(node.default_expr)

        return get_lca(expr_types + [else_type])

    @visitor.when(WhileNode)
    def visit(self, node):
        self.visit(node.condition)
        return self.visit(node.expression)
    
    @visitor.when(ForNode)
    def visit(self, node):
        iterable_protocol = self.context.get_protocol('Iterable')
        ttype = self.visit(node.iterable)

        expr_scope = node.expression.scope
        variable = expr_scope.find_variable(node.var)

        if ttype.is_unknow():
            variable.type = UnknowType()
        elif ttype.conforms_to(iterable_protocol):
            element_type = ttype.get_method('current').return_type
            variable.type = element_type
        else:
            variable.type = ErrorType()

        expr_type = self.visit(node.expression)
        return expr_type
    

    
    

    @visitor.when(VectorInitializationNode)
    def visit(self, node):
        elements_types = [self.visit(element) for element in node.elements]
        lca: Type = get_lca(elements_types)

        if lca.is_error():
            return ErrorType()
        
        elif lca.is_unknow():
            return UnknowType()

        return VectorType(lca)

    @visitor.when(VectorComprehensionNode)
    def visit(self, node):
        ttype = self.visit(node.iterable)
        iterable_protocol = self.context.get_protocol('Iterable')

        selector_scope = node.selector.scope
        variable = selector_scope.find_variable(node.var)

        if ttype.is_unknown():
            variable.type = UnknowType()

        elif ttype.conforms_to(iterable_protocol):
            element_type = ttype.get_method('current').return_type
            variable.type = element_type

        else:
            variable.type = ErrorType()

        return_type = self.visit(node.selector)

        if return_type.is_error():
            return ErrorType()
        
        elif return_type.is_unknow():
            return UnknowType()

        return VectorType(return_type)

    @visitor.when(IndexingNode)
    def visit(self, node):
        scope = node.scope

        number_type = self.context.get_type('Number')

        index_type = self.visit(node.index)
        obj_type = self.visit(node.obj)

        if index_type.is_unknow() and not index_type.is_error():
            self.pass_type(node.index.obj, scope, VectorType(number_type))

        elif index_type != number_type or index_type.is_error():
            return ErrorType()

        if obj_type.is_error():
            return ErrorType()
        
        elif obj_type.is_unknow():
            return UnknowType()

        if not isinstance(obj_type, VectorType):
            return ErrorType()

        return obj_type.get_element_type()


    def pass_type(self, node, scope: Scope, inf_type):
        if isinstance(node, VariableNode) and scope.is_defined(node.lex):
            variable = scope.find_variable(node.lex)
            if not variable.type.is_unknow() or variable.type.is_error():
                return
            variable.update_type(inf_type)






