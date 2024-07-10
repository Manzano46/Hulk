import cmp.cil as cil
from engine.code_generation.base import BaseHulkToCILVisitor
import cmp.visitor as visitor
from engine.language.ast_nodes import *

class HulkToCILVisitor(BaseHulkToCILVisitor):
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        ######################################################
        # node.declarations -> [ DeclarationNode ... ]
        # node.expression -> ExpressionNode
        ######################################################
        
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        self.main = self.register_function(main_method_name)
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
       # print(node.expression)
        self.register_instruction(cil.ReturnNode(self.visit(node.expression)))
        
        for feature in node.declarations: 
            self.visit(feature)
        

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node : TypeDeclarationNode):
        ######################################################
        # node.name -> string
        # node.methods -> [MethodDeclarationNode ... ]
        # node.attribute -> [AttributeDeclarationNode ... ]
        ######################################################
        
        self.current_type : Type = self.context.get_type(node.name)
        type_node = self.register_type(node.name)    
        
        for attribute, xtype in self.current_type.all_attributes():
            
            type_node.attributes.append(attribute.name)
        
        for method, xtype in self.current_type.all_methods():
            function_name = self.to_function_name(method.name, xtype.name)
            type_node.methods.append((method.name, function_name))
        
        # crear un constructor donde se setearan todos los atributos
        function_name = self.to_function_name('_init_', self.current_type.name)
        type_node.methods.append(('_init_', function_name))
        
        self.current_function : cil.FunctionNode = self.register_function(function_name)
        
        
        param_self = self.register_param(VariableInfo('self', self.current_type))
        #print('aquiiiiii ', self.current_type.params)
        for param in node.params:
            #print( ' hereeeee ',param, param.lex)
            #print(node.scope.children[0].find_variable(param.lex))
            self.register_param(node.scope.children[0].find_variable(param.lex))

        # llamar constructor del padre
        if self.current_type.parent is not None:
            self.register_instruction(cil.DynamicCallNode(self.current_type.parent.name, '_init_', param_self))
        
        for name, attribute in node.attributes:
            value = self.visit(attribute)
            self.register_instruction(cil.SetAttribNode(param_self, name, value))
        
        self.register_instruction(cil.ReturnNode(param_self))
        self.current_function = None
        
        for name,method in node.methods:
            self.visit(method)
        
        self.current_type = None
        
    @visitor.when(AttributeDeclarationNode)
    def visit(self, node : AttributeDeclarationNode):
        ######################################################
        # node.name -> string
        # node.expr -> ExpressionNode
        # node.attribute_type -> Type
        ######################################################
        
        value = self.visit(node.expr)
        return value
        
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node : MethodDeclarationNode):
        ######################################################
        # node.name -> string   
        # node.expr -> ExpressionNode
        # node.params -> [VariableNode ...]
        # node.return_type -> Type
        ######################################################
    
        self.current_method : Method = self.current_type.get_method(node.name)
        
        function_name = self.to_function_name(node.name, self.current_type.name)
        
        self.current_function : cil.FunctionNode = self.register_function(function_name)
        
        for param in node.params:
            var = node.scope.find_variable(param.lex)
            #print(var)
            self.register_param(var)
            
        value = self.visit(node.expr)
        self.register_instruction(cil.ReturnNode(value))
        
        self.current_function = None
        self.current_method = None
        
    @visitor.when(VarDeclarationNode)
    def visit(self, node : VarDeclarationNode):
        ######################################################
        # node.id -> string   
        # node.expr -> ExpressionNode
        # node.var_type -> Type
        ######################################################
        
        var = node.scope.find_variable(node.id)
        
        obj = self.register_local(var)
        xtype = var.type.name
        
        if xtype != 'Number':
            self.register_instruction(cil.AllocateNode(xtype, obj))
        
        value = self.visit(node.expr)
        
        self.register_instruction(cil.AssignNode(obj, value))
        
        return obj
    
    @visitor.when(LetInNode)
    def visit(self, node : LetInNode):
        ######################################################
        # node.var_declarations -> [VarDeclarationNode]
        # node.expr -> ExpressionNode
        ######################################################
        
        for declaration in node.var_declarations:
            self.visit(declaration)
            
        #(node.expr, 'aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
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
            return VoidType()
        else:
            for arg in node.args:
                value = self.visit(arg)
                self.register_function(cil.ArgNode(value))
            var = self.define_internal_local()
            self.register_instruction(cil.StaticCallNode(node.idx,  var))
            return var    
            
        
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
    
    @visitor.when(ConditionalNode)
    def visit(self, node : ConditionalNode):
        ######################################################
        # node.conditional_expression_list -> [ExpressionNode]
        # node.else_expr ->
        ######################################################
        
        dif = self.labels # <----
        
        return_ = self.define_internal_local()
        
        for (it,(condition, expression)) in enumerate(node.condition_expression_list):
            cond = self.visit(condition)
            #print(cond, condition)
            
            self.register_instruction(cil.GotoIfNode(cond, f'label_{self.labels}' ))
            #dif = self.labels - it
            self.labels += 1
        
        
        else_ = self.visit(node.else_expr)
        self.register_instruction(cil.AssignNode(return_, else_))
        self.register_instruction(cil.GotoNode(f'label_{self.labels}'))
            
        for (it,(condition, expression)) in enumerate(node.condition_expression_list):
            
            label = dif + it
            self.register_instruction(cil.LabelNode(f'label_{label}'))
            
            expr = self.visit(expression)
            self.register_instruction(cil.AssignNode(return_, expr))
            
            self.register_instruction(cil.GotoNode(f'label_{self.labels}'))
            
        self.register_instruction(cil.LabelNode(self.labels))
        self.labels += 1
        
        return return_
    
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
    
    @visitor.when(DestructiveAssignmentNode)
    def visit(self, node : DestructiveAssignmentNode):
        ######################################################
        # node.var -> string
        # node.expr -> ExpressionNode
        ######################################################
        
        value = self.visit(node.expr)
        
        var = self.find(node.var)
        
        self.register_instruction(cil.AssignNode(var, value))
        return var
    
    @visitor.when(FunctionDeclarationNode)
    def visit(self, node : FunctionDeclarationNode):
        ######################################################
        # node.id -> string
        # node.param -> [VariableNode ...]
        # node.expr -> ExpressionNode
        # node.return_type -> Type
        ######################################################
        
        parent = self.current_function
        
        self.current_function = self.register_function(node.id, node.type)
        
        for param in node.params:
            var = node.scope.find_variable(param.lex)
            self.register_param(var)
        
        expr = self.visit(node.expr)
        self.register_instruction(cil.ReturnNode(expr))
        
        self.current_function = parent
        
    @visitor.when(TypeInstantiationNode)
    def visit(self, node : TypeInstantiationNode):
        ######################################################
        # node.idx -> string
        # node.args -> [ExpressionNode ...]
        ######################################################
        
        var = self.define_internal_local()
        type_ = None
        for x in self.dottypes:
            if x.name == node.idx:
                type_ = x
        self.register_instruction(cil.AllocateNode(type_, var))
        return var
    
    