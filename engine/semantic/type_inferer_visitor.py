import cmp.visitor as visitor
from cmp.semantic import *
from engine.language.ast_nodes import *
from engine.semantic.semantic_tools import get_lca, get_lower_heir

class TypeInferer(object):
    def __init__(self, context, errors=[]):
        self.errors = errors
        self.context = context
        self.current_type = None
        self.current_method = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for _ in range(5):
            for declaration in node.declarations:
                self.visit(declaration)

            self.visit(node.expression)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        self.current_type: Type = self.context.get_type(node.name)

        if self.current_type.is_error():
            return
        
        parent_args_types = [self.visit(arg) for arg in node.parent_args]
        if self.current_type.parent and not self.current_type.parent.is_error():
            for arg, arg_type in zip(node.parent_args, self.current_type.parent.params_type):
                self.pass_type(arg, arg.scope, arg_type)

            for i, param_type in enumerate(self.current_type.parent.params_type):
                if len(parent_args_types) <= i:
                        break
                
                arg = parent_args_types[i]
                if param_type.is_unknow() and not param_type.is_error():
                    var = self.current_type.parent.param_vars[i]
                    var.infer(arg)

        for _, attribute in node.attributes:
            self.visit(attribute)

        const_scope = node.scope.children[0]
        for i, param_type in enumerate(self.current_type.params_type):
            param_name = self.current_type.params[i]
            local_var = const_scope.find_variable(param_name)
            local_var.type = param_type

            # Check if we could infer the param type in the body
            if param_type.is_unknow() and local_var.is_param and local_var.infered_types:
                try:
                    new_type = get_lower_heir(local_var.infered_types, var_name=param_name)
                except SemanticError as e:
                    self.errors.append(e)
                    new_type = ErrorType()
                self.current_type.params_type[i] = new_type
                if not new_type.is_unknow():
                    self.had_changed = True

                local_var.update_type(new_type)

            # Check if we could infer the param type in a call
            if (self.current_type.params_type[i].is_unknow() and self.current_type.param_vars[i].infered_types):
                new_type = get_lca(self.current_type.param_vars[i].infered_types)
                self.current_type.params_type[i] = new_type
                if not new_type.is_unknow():
                    pass
                local_var.update_type(new_type)

        # Infer the params types and return type of the methods
        for _, method in node.methods:
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
    def visit(self, node: MethodDeclarationNode):
        #print("Method Declaration ", node.name)
        self.current_method = self.current_type.get_method(node.name)

        method_scope: Scope = node.expr.scope
        return_type = self.visit(node.expr)

        if self.current_method.return_type.is_unknow() and not self.current_method.return_type.is_error() and (
               not return_type.is_unknow() or return_type.is_error()):
            self.current_method.return_type = return_type

        # Check if we could infer some params types
        for i, param_type in enumerate(self.current_method.param_types):
            param_name = self.current_method.param_names[i]
            local_var = method_scope.find_variable(param_name)
            local_var.type = param_type

            # Check if we could infer the param type in the body
            if param_type.is_unknow() and local_var.is_param and local_var.infered_types:
                try:
                    new_type = get_lower_heir(local_var.infered_types, var_name=param_name)
                except SemanticError as e:
                    self.errors.append(e)
                    new_type = ErrorType()

                self.current_method.param_types[i] = new_type
                local_var.update_type(new_type)

            # Check if we could infer the param type in a call
            if (self.current_method.param_types[i].is_unknow()
                    and self.current_method.param_vars[i].infered_types):
                new_type = get_lca(self.current_method.param_vars[i].infered_types)
                self.current_method.param_types[i] = new_type
                if not new_type.is_unknow():
                    self.had_changed = True
                local_var.update_type(new_type)

        self.current_method = None
        return return_type
    

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        function = self.context.get_function(node.id)

        return_type: Type = self.visit(node.expr)
        # print(return_type)

        if function.return_type.is_unknow() and not function.return_type.is_error() and not return_type.is_unknow():
            function.return_type = return_type

        expr_scope: Scope = node.expr.scope

        # Check if we could infer some params types
        for i, param_type in enumerate(function.param_types):
            param_name = function.param_names[i]
            local_var = expr_scope.find_variable(param_name)
            local_var.type = param_type
            # Check if we could infer the param type in the body
            if param_type.is_unknow() and local_var.is_param and local_var.infered_types:
                try:
                    new_type: Type = get_lower_heir(param_name, local_var.infered_types)

                except SemanticError as e:
                    self.errors.append(e)
                    new_type: Type = ErrorType()

                function.param_types[i] = new_type
                # if not new_type.is_unknow():
                #     self.had_changed = True

                local_var.update_type(new_type)

            # Check if we could infer the param type in a call
            if function.param_types[i].is_unknow() and function.param_vars[i].infered_types:
                new_type = get_lca(function.param_vars[i].infered_types)
                function.param_types[i] = new_type

                # if not new_type.is_unknow():
                #     self.had_changed = True

                local_var.update_type(new_type)

        return return_type
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node):
        expr_type = ErrorType()
        for expr in node.expressions:
            expr_type = self.visit(expr)
        return expr_type
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode):
        # print("VarDeclaration Node", node.id)

        inf_type = self.visit(node.expr)
        var = node.scope.find_variable(node.id)
        # print(var.name, var.type)
        var.type = var.type if not var.type.is_unknow() or var.type.is_error() else inf_type
        return var.type

    @visitor.when(LetInNode)
    def visit(self, node):
        # print("Node Let In")
        for declaration in node.var_declarations:
            self.visit(declaration)
        return self.visit(node.expr)
    
    @visitor.when(DestructiveAssignmentNode)
    def visit(self, node):
        # print("Destructive")
        new_type = self.visit(node.expr)
        old_type = self.visit(node.var)

        if old_type.name == 'Self':
            return ErrorType()

        if new_type.is_unknow() and not old_type.is_unknow():
            self.pass_type(node.expr, node.scope, old_type)

        return old_type
    
    @visitor.when(ConditionalNode)
    def visit(self, node):
        for cond,_ in node.condition_expression_list:
            self.visit(cond)

        expr_types = [self.visit(expression) for _,expression in node.condition_expression_list]

        else_type = self.visit(node.else_expr)

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
    
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode):
        scope: Scope = node.scope

        args_types: list[Type] = [self.visit(arg) for arg in node.args]

        try:
            function = self.context.get_function(node.idx)

        except SemanticError:
            return ErrorType()

        for arg, param_type in zip(node.args, function.param_types):
            self.pass_type(arg, scope, param_type)

        for i, func_param_type in enumerate(function.param_types):
            if len(args_types) <= i:
                break

            arg: Type = args_types[i]
            if func_param_type.is_unknow() and not func_param_type.is_error():
                var = function.param_vars[i]
                var.infer(arg)

        return function.return_type
    
    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode):
        scope: Scope = node.scope

        if self.current_method is None:
            return ErrorType()

        args_types: list[Type] = [self.visit(arg) for arg in node.args]

        try:
            method: Method = self.current_type.parent.get_method(self.current_method.name)

        except SemanticError:
            return ErrorType()

        for arg, param_type in zip(node.args, method.param_types):
            self.pass_type(arg, scope, param_type)

        for i, func_param_type in enumerate(method.param_types):
            if len(args_types) <= i:
                break

            arg: Type = args_types[i]
            if func_param_type.is_unknow() and not func_param_type.is_error():
                var = method.param_vars[i]
                var.infer(arg)

        return method.return_type
    
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode):
        scope: Scope = node.scope
        obj_type: Type = self.visit(node.obj)

        if obj_type.is_error():
            return ErrorType()

        args_types: list[Type] = [self.visit(arg) for arg in node.args]

        try:
            if obj_type == SelfType():
                method: Method = self.current_type.get_method(node.method)
            else:
                method: Method = obj_type.get_method(node.method)

        except SemanticError:
            return ErrorType()

        for arg, param_type in zip(node.args, method.param_types):
            self.pass_type(arg, scope, param_type)

        for i, method_param_type in enumerate(method.param_types):
            if len(args_types) <= i:
                break

            arg: Type = args_types[i]
            if method_param_type.is_unknow() and not method_param_type.is_error():
                var = method.param_vars[i]
                var.infer(arg)

        return method.return_type


    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode):
        #print('attr call node')
        obj_type: Type = self.visit(node.obj)

        if obj_type.is_error():
            return ErrorType()

        if obj_type == SelfType():
            try:
                attr: Attribute = self.current_type.get_attribute(node.attribute)
                return attr.type

            except SemanticError:
                return ErrorType()
        else:
            # Can't access to a non-self attribute
            return ErrorType()

    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        bool_type = self.context.get_type('Boolean')
        self.visit(node.expression)
        return bool_type

    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        expr_type = self.visit(node.expression)

        try:
            cast_type = self.context.get_type_or_protocol(node.ttype)

        except SemanticError:
            cast_type = ErrorType()

        if expr_type.is_unknow() and not expr_type.is_error():
            return cast_type

        return cast_type


    @visitor.when(ArithmeticExpressionNode)
    def visit(self, node: ArithmeticExpressionNode):
        # print("Arithmetic Node")
        scope: Scope = node.scope

        number_type: Type = self.context.get_type('Number')

        left_type: Type = self.visit(node.left)
        right_type: Type = self.visit(node.right)

        if left_type.is_unknow() and not left_type.is_error():
            self.pass_type(node.left, scope, number_type)

        elif left_type != number_type or left_type.is_error():
            return ErrorType()

        if right_type.is_unknow() and not right_type.is_error():
            self.pass_type(node.right, scope, number_type)

        elif right_type != number_type or right_type.is_error():
            return ErrorType()

        return number_type


    @visitor.when(InequalityExpressionNode)
    def visit(self, node: ArithmeticExpressionNode):
        scope: Scope = node.scope

        bool_type: Type = self.context.get_type('Boolean')
        number_type: Type = self.context.get_type('Number')

        left_type: Type = self.visit(node.left)
        right_type: Type = self.visit(node.right)

        if left_type.is_unknow() and not left_type.is_error():
            self.pass_type(node.left, scope, number_type)

        elif left_type != number_type or left_type.is_error():
            return ErrorType()

        if right_type.is_unknow() and not right_type.is_error():
            self.pass_type(node.right, scope, number_type)

        elif right_type != number_type or right_type.is_error():
            return ErrorType()

        return bool_type


    @visitor.when(BoolBinaryExpressionNode)
    def visit(self, node: BoolBinaryExpressionNode):
        scope: Scope = node.scope

        bool_type: Type = self.context.get_type('Boolean')

        left_type: Type = self.visit(node.left)
        right_type: Type = self.visit(node.right)

        if left_type.is_unknow() and not left_type.is_error():
            self.pass_type(node.left, scope, bool_type)

        elif left_type != bool_type or left_type.is_error():
            return ErrorType()

        if right_type.is_unknow() and not right_type.is_error():
            self.pass_type(node.right, scope, bool_type)

        elif right_type != bool_type or right_type.is_error():
            return ErrorType()

        return bool_type


    @visitor.when(StrBinaryExpressionNode)
    def visit(self, node: StrBinaryExpressionNode):
        scope: Scope = node.scope

        string_type: Type = self.context.get_type('String')
        object_type: Type = self.context.get_type('Object')

        left_type: Type = self.visit(node.left)
        right_type: Type = self.visit(node.right)

        if left_type.is_unknow() and not left_type.is_error():
            self.pass_type(node.left, scope, object_type)
            
        elif left_type.is_error():
            return ErrorType()

        if right_type.is_unknow() and not right_type.is_error():
            self.pass_type(node.right, scope, object_type)

        elif right_type.is_error():
            return ErrorType()

        return string_type

    @visitor.when(EqualityExpressionNode)
    def visit(self, node: EqualityExpressionNode):

        bool_type: Type = self.context.get_type('Boolean')
        _ = self.visit(node.left)
        _ = self.visit(node.right)

        return bool_type

    @visitor.when(NegNode)
    def visit(self, node: NegNode):
        scope = node.scope

        operand_type: Type = self.visit(node.operand)
        number_type: Type = self.context.get_type('Number')

        if operand_type.is_unknow():
            self.pass_type(node.operand, scope, number_type)

        elif operand_type != number_type or operand_type.is_error():
            return ErrorType()

        return number_type

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        scope = node.scope

        operand_type: Type = self.visit(node.operand)
        bool_type: Type = self.context.get_type('Boolean')

        if operand_type.is_unknow() and not operand_type.is_error():
            self.pass_type(node.operand, scope, bool_type)

        elif operand_type != bool_type or operand_type.is_error():
            return ErrorType()

        return bool_type

    @visitor.when(BooleanNode)
    def visit(self, node):
        return self.context.get_type('Boolean')

    @visitor.when(NumberNode)
    def visit(self, node):
        # print("Number node ")
        return self.context.get_type('Number')

    @visitor.when(StringNode)
    def visit(self, node):
        return self.context.get_type('String')
    
    @visitor.when(VariableNode)
    def visit(self, node: VariableNode):
        scope: Scope = node.scope

        if not scope.is_defined(node.lex):
            return ErrorType()

        var = scope.find_variable(node.lex)
        return var.type
    
    @visitor.when(TypeInstantiationNode)
    def visit(self, node):
        args_types = [self.visit(arg) for arg in node.args]

        try:
            type: Type = self.context.get_type(node.idx)

        except SemanticError:
            return ErrorType()

        if type.is_error():
            return ErrorType()

        for arg, param_type in zip(node.args, type.params_type):
            self.pass_type(arg, node.scope, param_type)

        for i, param_type in enumerate(type.params_type):
            if len(args_types) <= i:
                break
            arg = args_types[i]

            if param_type.is_unknow() and not param_type.is_error():
                var = type.param_vars[i]
                var.infer(arg)

        return type

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

        if ttype.is_unknow():
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
            variable.infer(inf_type)






