from cmp.semantic import Scope, VariableInfo
from cmp.semantic import Context
import cmp.visitor as visitor
from engine.language.ast_nodes import *
import copy
    

class RuntimeError(Exception):
    @property
    def msg(self):
        mess = ''.join(' ' + str(x) for x in self.args)
        return mess

class HulkInterpreter:
    
    def __init__(self, context) -> None:
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context : Context = context
        self.errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        ######################################################
        # node.declarations -> [ DeclarationNode ... ]
        # node.expression -> ExpressionNode
        ######################################################
        
        for feature in node.declarations: 
            self.visit(feature)
        
        return self.visit(node.expression)

    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node : TypeDeclarationNode):
        ######################################################
        # node.name -> string
        # node.methods -> [MethodDeclarationNode ... ]
        # node.attribute -> [AttributeDeclarationNode ... ]
        ######################################################
        
        return node
        
    @visitor.when(AttributeDeclarationNode)
    def visit(self, node : AttributeDeclarationNode):
        ######################################################
        # node.name -> string
        # node.expr -> ExpressionNode
        # node.attribute_type -> Type
        ######################################################
        var = node.scope.define_variable(f'self.{node.name}')
        #var = node.scope.find_variable(node.name)
        value = self.visit(node.expr)
        var.value = var
        return 
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node : MethodDeclarationNode):
        ######################################################
        # node.name -> string   
        # node.expr -> ExpressionNode
        # node.params -> [VariableNode ...]
        # node.return_type -> Type
        ######################################################
    
        return
    
    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node : ProtocolDeclarationNode):
        ######################################################
        # node.idx -> string   
        # node.method_signature -> MethodSignatureNode
        # node.parent -> ProtocolDeclarationNode
        ######################################################
        
        return
    
    @visitor.when(FunctionDeclarationNode)
    def visit(self, node : FunctionDeclarationNode):
        ######################################################
        # node.id -> string   
        # node.expr -> ExpressionNode
        # node.return_type -> Type
        ######################################################
        
        return
        
    @visitor.when(VarDeclarationNode)
    def visit(self, node : VarDeclarationNode):
        ######################################################
        # node.id -> string   
        # node.expr -> ExpressionNode
        # node.var_type -> Type
        ######################################################
        
        var = node.scope.find_variable(node.id)
        val = self.visit(node.expr)
        var.value = val
        return 
    
    @visitor.when(VectorInitializationNode)
    def visit(self, node: VectorInitializationNode):
        return
    
    @visitor.when(LetInNode)
    def visit(self, node : LetInNode):
        ######################################################
        # node.var_declarations -> [VarDeclarationNode]
        # node.expr -> ExpressionNode
        ######################################################
        
        for declaration in node.var_declarations:
            self.visit(declaration)
            
        return self.visit(node.expr)
    
    @visitor.when(PlusNode)
    def visit(self, node : PlusNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.PlusNode(result, left, right))
        
        return result
    
    
    @visitor.when(MinusNode)
    def visit(self, node : MinusNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.MinusNode(result, left, right))
        
        return result
    
    @visitor.when(DivNode)
    def visit(self, node : DivNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.DivNode(result, left, right))
        
        return result
    
    @visitor.when(StarNode)
    def visit(self, node : StarNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.StarNode(result, left, right))
        
        return result
    
    @visitor.when(PowNode)
    def visit(self, node : PowNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.PowNode(result, left, right))
        
        return result
    
    @visitor.when(ModNode)
    def visit(self, node : ModNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.ModNode(result, left, right))
        
        return result
    
    @visitor.when(NumberNode)
    def visit(self, node : NumberNode):
        ######################################################
        # node.lex -> string
        ######################################################
        
        return node.lex
    
    @visitor.when(StringNode)
    def visit(self, node : StringNode):
        ######################################################
        # node.lex -> string
        ######################################################
        
        #print('string')
        
        var = self.find_cte(node.lex)
        if var == None:
            var = self.register_local_cte(node.lex)
        
        constant = None
        for data in self.dotdata:
            if data.value == node.lex:
                constant = data.name 
                
        if constant == None:
            cte = self.register_data(node.lex)
            self.register_instruction(cil.LoadNode(var, cte.name))
        
        return var
    
    @visitor.when(BooleanNode)
    def visit(self, node : BooleanNode):
        ######################################################
        # node.lex -> string
        ######################################################
        
        if node.lex == 'True':
            return 1
        else:
            return 0
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node : ExpressionBlockNode):
        ######################################################
        # node.expressions -> [ExpressionNode ...]
        ######################################################
        
        value = None
        for expr in node.expressions:
            value = self.visit(expr)
        
        return value
    
    @visitor.when(VariableNode)
    def visit(self, node : VariableNode):
        ######################################################
        # node.lex -> string
        # node.type -> Type
        ######################################################
        
        var = self.find(node.lex)
        
        return var
    
    # @visitor.when(PrintNode)
    # def visit(self, node : PrintNode):
    #     ######################################################
    #     # node.expr -> ExpressionNode
    #     ######################################################
    #     print('print')
    #     value = self.visit(node.expr)
        
    #     self.register_instruction(cil.PrintNode(value))
        
    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode):
        ######################################################
        # node.idx -> string
        # node.args -> [ExpressionNode ...]
        ######################################################
        #print('functionCall')
        if node.idx == 'print':
            self.register_instruction(cil.PrintNode(self.visit(node.args[0])))
        else:
            for arg in node.args:
                value = self.visit(arg)
                self.register_function(cil.ArgNode(value))
        
    @visitor.when(DestructiveAssignmentNode)
    def visit(self, node: DestructiveAssignmentNode):
        
        variable = node.scope.find_variable(node.var.lex)
        value = self.visit(node.expression)
        variable.update(value)
        return value
        
    @visitor.when(ConcatNode)
    def visit(self, node : ConcatNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.ConcatNode(result, left, right))
        
        return result
    
    @visitor.when(TypeInstantiationNode)
    def visit(self, node: TypeInstantiationNode):
        
        type_node = self.context.get_type(node.identifier).curr_node
        
        type_node: TypeDeclarationNode = copy.deepcopy(type_node)

        args_ = [self.visit(i) for i in node.args]
        parent = type_node

        while parent:
            scope = parent.scope
            
            for i, vname in enumerate(parent.param_ids):
                var = scope.define_variable(vname, None)
                var.value = args_[i]

            for attr in parent.attributes:
                var = scope.define_variable(f"self.{attr.identifier}", None)
                value = self.visit(attr.expression)
                var.value = value

            for method in parent.methods:
                method: MethodDeclarationNode

                scope.define_function(method.identifier, method.param_ids, method.param_types, method.type,body=method.expression,
                )

            if len(parent.type_parent_args) > 0:
                args = [self.visit(arg) for arg in parent.type_parent_args]

            
            if parent.parent:
                oldChild = parent
                parent: TypeDeclarationNode = self.context.get_type(
                    parent.parent, len(parent.type_parent_args)
                ).current_node
                parent = copy.deepcopy(parent)
                scope.parent = parent.scope  

                for p_method in parent.methods:
                    for c_method in oldChild.methods:
                        if p_method.identifier == c_method.identifier:
                            c_method.scope.define_function(
                                fname="base",
                                param_names=p_method.param_ids,
                                param_types=p_method.param_types,
                                return_type=p_method.type,
                                body=p_method.expression,
                            )
            else:
                break
        return type_node

    
    
    @visitor.when(ConditionalNode)
    def visit(self, node : ConditionalNode):
        ######################################################
        # node.conditional_expression_list -> [ExpressionNode]
        # node.else_expr ->
        ######################################################
        
        for expr, cond in zip(node.condition_expression_list, node.condition_expression_list):
            if self.visit(cond):
                return self.visit(expr)
            return self.visit(node.else_expr)
    
    @visitor.when(EqualNode)
    def visit(self, node : EqualNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.EqualNode(result, left, right))
        
        return result
    
    @visitor.when(NotEqualNode)
    def visit(self, node : EqualNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.NotEqualNode(result, left, right))
        
        return result
    
    @visitor.when(GreaterOrEqualNode)
    def visit(self, node : GreaterOrEqualNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.GreaterOrEqualNode(result, left, right))
        
        return result
    
    @visitor.when(LessOrEqualNode)
    def visit(self, node : LessOrEqualNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.LessOrEqualNode(result, left, right))
        
        return result
    
    @visitor.when(LessThanNode)
    def visit(self, node : LessThanNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.LessThanNode(result, left, right))
        
        return result
    
    @visitor.when(GreaterThanNode)
    def visit(self, node : GreaterThanNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        result = self.define_internal_local()
        left = self.visit(node.left)
        right = self.visit(node.right)
        self.register_instruction(cil.GreaterThanNode(result, left, right))
        
        return result
    
    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        res = None
        while self.visit(node.condition):
            res = self.visit(node.expression)
        return res
    
    @visitor.when(ForNode)
    def visit(self, node: ForNode):
        evaluation = None
        it: VariableInfo = node.expression.scope.find_variable(node.var)

        for variable in self.visit(node.iterable):
            it.value = variable
            res = self.visit(node.expression)
        return res
    
    
    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        value = self.visit(node.expression)

        type = self.context.get_type(node.type.lexeme)
        if isinstance(value, float):
            return type == "Number"
        elif isinstance(value, str):
            return type == "String"
        elif isinstance(value, bool):
            return type == "Bool"
        elif isinstance(value, list):
            return type == "Vector"
        else:
            try:
                value: TypeDeclarationNode
                args_len = len(value.param_ids)
                while value:
                    if value.identifier == node.type.lexeme:
                        return True
                    if value.parent:
                        value = value.parent
                        value = self.context.get_type(value, args_len).current_node
                    else:
                        value = None
            except Exception as e:
                # print("ERROR IS")
                return False
            
            
    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        value = self.visit(node.expression)
        value: TypeDeclarationNode
        tmp = value
        while tmp.identifier != node.type.lexeme:
            if tmp.parent:
                tmp = self.context.get_type(
                    tmp.parent, len(tmp.type_parent_args)
                ).current_node
            else:
                break
        node.scope = tmp.scope
        return node