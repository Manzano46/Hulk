from cmp.semantic import Scope, VariableInfo
from cmp.semantic import Context
import cmp.visitor as visitor
from engine.language.ast_nodes import *
import copy
import math
import random

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
        self.program_node = None
        # self.errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        ######################################################
        # node.declarations -> [ DeclarationNode ... ]
        # node.expression -> ExpressionNode
        ######################################################
        
        # for feature in node.declarations: 
        #     self.visit(feature)
        self.program_node = node
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
        var.value = value
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
        return [self.visit(element) for element in node.elements]
    
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
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left + right
    
    
    @visitor.when(MinusNode)
    def visit(self, node : MinusNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left - right
    
    @visitor.when(DivNode)
    def visit(self, node : DivNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left/right
    
    @visitor.when(StarNode)
    def visit(self, node : StarNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left * right
    
    @visitor.when(PowNode)
    def visit(self, node : PowNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left ** right
    
    @visitor.when(ModNode)
    def visit(self, node : ModNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left % right
    
    @visitor.when(NumberNode)
    def visit(self, node : NumberNode):
        ######################################################
        # node.lex -> string
        ######################################################
        
        return float(node.lex)
    
    @visitor.when(StringNode)
    def visit(self, node : StringNode):
        ######################################################
        # node.lex -> string
        ######################################################
        
        return node.lex
    
    @visitor.when(BooleanNode)
    def visit(self, node : BooleanNode):
        ######################################################
        # node.lex -> string
        ######################################################

        if node.lex == 'True':
            return True
        else:
            return False
    
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
        var = node.scope.find_variable(node.lex)
        # print(node.lex, var.value)
        return var.value
        
    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode):
        ######################################################
        # node.idx -> string
        # node.args -> [ExpressionNode ...]
        ######################################################
        args_list = [self.visit(arg) for arg in node.args]
        print('function ', node.idx, args_list)
        if node.idx == 'print':
            print(*args_list)
            return None
        elif node.idx == 'sqrt':
            return math.sqrt(*args_list)
        elif node.idx == 'sin':
            return math.sin(*args_list)
        elif node.idx == 'cos':
            return math.cos(*args_list)
        elif node.idx == 'exp':
            return math.exp(*args_list)
        elif node.idx == 'log':
            return math.log(*args_list)
        elif node.idx == 'rand':
            return random.random()
        else:
            fdecl_ = None
            for func in self.program_node.declarations:
                if (isinstance(func, FunctionDeclarationNode) and 
                    func.id == node.idx and len(args_list)==len(func.params)):
                    fdecl_ = copy.deepcopy(func)
                    break
            
            fdecl_.scope.parent = node.scope
            obj_func = self.context.get_function(node.idx)
            for i, var in enumerate(obj_func.param_vars):
                variable = fdecl_.scope.children[0].define_variable(var.name, var.type)
                variable.value = args_list[i]
            
            return self.visit(fdecl_.expr)
            
    @visitor.when(DestructiveAssignmentNode)
    def visit(self, node: DestructiveAssignmentNode):
        value = self.visit(node.expr)

        if isinstance(node.var, AttributeCallNode):
            variable = node.scope.find_variable(node.var.obj.lex)
            variable.value[node.var.attribute] = value
        else:
            variable = node.scope.find_variable(node.var.lex)
            variable.update_value(value)

        return value
        
    @visitor.when(ConcatNode)
    def visit(self, node : ConcatNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left + right
    
    @visitor.when(TypeInstantiationNode)
    def visit(self, node: TypeInstantiationNode):
        
        type_ = self.context.get_type(node.idx)
        type__ = type_
        type_node: TypeDeclarationNode = copy.deepcopy(type_.curr_node)
        obj = {"type": type_node}

        args_ = [self.visit(i) for i in node.args]
        parent = type_node

        while parent:
            scope = parent.scope
            
            for i, vname in enumerate(parent.params):
                var = scope.define_variable(vname, type__.param_vars[i].type)
                var.value = args_[i]

            for attr, expr in parent.attributes:
                # var = scope.define_variable(f"self.{attr.identifier}", None)
                value = self.visit(expr.expr)
                obj[attr] = value
                # var.value = value

            # for method in parent.methods:
            #     method: MethodDeclarationNode

            #     scope.define_function(method.identifier, method.param_ids, method.param_types, method.type,body=method.expression,
            #     )

            # if len(parent.type_parent_args) > 0:
            #     args = [self.visit(arg) for arg in parent.type_parent_args]

            
            if parent.parent:
                oldChild = parent
                type__ = self.context.get_type(parent.parent)
                parent: TypeDeclarationNode = copy.deepcopy(type__.curr_node)
                scope.parent = parent.scope  

                # for p_method in parent.methods:
                #     for c_method in oldChild.methods:
                #         if p_method.identifier == c_method.identifier:
                #             c_method.scope.define_function(
                #                 fname="base",
                #                 param_names=p_method.param_ids,
                #                 param_types=p_method.param_types,
                #                 return_type=p_method.type,
                #                 body=p_method.expression,
                #             )
            else:
                break
        return obj
    
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode):
        # print('buscando ', node.obj.lex)
        obj = node.scope.find_variable(node.obj.lex)
        obj_meth = obj.type.get_method(node.method)
        # print('buscando metodo ', node.method)
        sself = node.scope.define_variable('self', obj.type)
        sself.value = obj.value

        method = obj_meth.curr_node
        method.scope.parent = node.scope

        # object_instance: TypeDeclarationNode = node.scope.get_global_variable_info(
        #     variable_name
        # ).value

        args_ = [self.visit(expr) for expr in node.args]
        for i, var in enumerate(obj_meth.param_vars):
            variable = method.scope.define_variable(var.name, var.type)
            variable.value = args_[i]

        result = self.visit(method.expr)

        # if isinstance(object_instance, list):
        #     if node.method_identifier == "next":
        #         if len(object_instance) == 0:
        #             return False
        #         return True
        #     if node.method_identifier == "current":
        #         return object_instance.pop(0)

        # print(" ------------------------------- MethodCallNode - - - -- - - -- - - - ")
        # print("variable name: ", variable_name)
        # print("value :", object_instance)
        # print("id: ", node.object_identifier.lexeme)
        # print("mid:", node.method_identifier)
        # print("-----------------------------DEBUG OFFF ---------------------")

        # if object_instance is None and variable_name == "self":
        #     object_instance = node
            # print(
            #     'object_instance is None and variable_name == "self"',
            #     [i.name for i in node.scope.get_all_functions()],
            # )

        # method: Function = object_instance.scope.get_global_function_info(
        #     node.method_identifier, len(node.args)
        # )

        # method.body = copy.deepcopy(method.body)

        # old_scope_locals = copy.deepcopy(method.body.scope.local_vars)
        # print(
        #     "= = = " * 5,
        #     str([(i.name, i.value) for i in method.body.scope.get_all_variables()]),
        # )
        # for i, vname in enumerate(method.param_names):
        #     value = self.visit(node.args[i])
        #     method.body.scope.get_global_variable_info(vname).update(value)
        # print(
        #     method.name,
        #     method.body,
        #     str([(i.name, i.value) for i in method.body.scope.get_all_variables()]),
        # )
        # value = self.visit(method.body)
        # method.body.scope.local_vars = old_scope_locals
        # return value
        return result
    
    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode):
        val =  node.scope.find_variable(node.obj.lex).value[node.attribute]
        return val
    
    
    @visitor.when(ConditionalNode)
    def visit(self, node : ConditionalNode):
        ######################################################
        # node.conditional_expression_list -> [ExpressionNode]
        # node.else_expr ->
        ######################################################
        
        for cond, expr in node.condition_expression_list:
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
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left == right
    
    @visitor.when(NotEqualNode)
    def visit(self, node : EqualNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left != right
    
    @visitor.when(GreaterOrEqualNode)
    def visit(self, node : GreaterOrEqualNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left >= right
    
    @visitor.when(LessOrEqualNode)
    def visit(self, node : LessOrEqualNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left <= right
    
    @visitor.when(LessThanNode)
    def visit(self, node : LessThanNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left < right
    
    @visitor.when(GreaterThanNode)
    def visit(self, node : GreaterThanNode):
        ######################################################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        # node.operator -> String
        ######################################################
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        return left > right
    
    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        # print('whilenode')
        res = None
        while self.visit(node.condition):
            res = self.visit(node.expression)
        return res
    
    @visitor.when(ForNode)
    def visit(self, node: ForNode):
        evaluation = None
        it: VariableInfo = node.expression.scope.find_variable(node.var)

        for variable in self.visit(node.iterable):
            it.update_value(variable)
            res = self.visit(node.expression)

        return res
    
    
    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        value = self.visit(node.expression)

        type = self.context.get_type(node.ttype)

        if isinstance(value, float):
            return type.name == "Number"
        elif isinstance(value, str):
            return type.name == "String"
        elif isinstance(value, bool):
            return type.name == "Boolean"
        elif isinstance(value, list):
            return type.name == "Vector"
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
    
    @visitor.when(IndexingNode)
    def visit(self, node: IndexingNode):
        index = self.visit(node.index)
        vector = node.scope.find_variable(node.obj).value
        try:
            int_index = int(index)
        except Exception as e:
            print(f"💥Runtime Error: Index out of range in {node.obj}")
            exit(1)
        return vector[int_index]