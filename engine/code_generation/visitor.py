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
        
        print(node.expression)
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
        
        param_self = self.register_param('self')
        
        # llamar constructor del padre
        result = self.define_internal_local()
        self.register_instruction(cil.DynamicCallNode(self.current_type.parent, '_init_', result))
        
        for attribute in node.attributes:
            value = self.visit(attribute)
            self.register_instruction(cil.SetAttribNode(param_self, attribute.name, value))
        
        self.register_instruction(cil.ReturnNode(param_self))
        self.current_function = None
        
        for method in node.methods:
            self.visit(method)
        
        self.current_type = None
        
    @visitor.when(AttributeDeclarationNode)
    def visit(self, node : AttributeDeclarationNode):
        ######################################################
        # node.name -> string
        # node.expr -> ExpressionNode
        # node.attribute_type -> Type
        ######################################################
        
        
        obj = self.register_local(node.name)
        value = self.visit(node.expr)
        self.register_instruction(cil.AssignNode(obj, value))
        
        return obj
    
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
            self.register_param(param.lex)
            
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
            
        print(node.expr, 'aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
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
        
        print('string')
        
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
        print('functionCall')
        if node.idx == 'print':
            self.register_instruction(cil.PrintNode(self.visit(node.args[0])))
        else:
            for arg in node.args:
                value = self.visit(arg)
                self.register_function(cil.ArgNode(value))
        