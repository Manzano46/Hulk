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
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
        for feature, child_scope in node.declarations + [node.expression]:
            self.visit(feature, child_scope)

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
        
        for feature, child_scope in node.attributes + node.methods:
            self.visit(feature, child_scope)
        
        self.current_type = None