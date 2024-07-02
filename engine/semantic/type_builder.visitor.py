
import cmp.visitor as visitor
from cmp.semantic import SemanticError, Context, ErrorType
from engine.language.ast_nodes import *

# Let's collect the attributes and methods of each of the defined types

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.name)
        except SemanticError as e:
            self.errors.append(e.text)
            self.current_type = ErrorType()

        if node.parent != None:
            try:
                current_parent_type = self.context.get_type(node.parent)
            except SemanticError as e:
                self.errors.append(e.text)
                current_parent_type = ErrorType()
            try:
                self.current_type.set_parent(current_parent_type)
            except SemanticError as e:
                self.errors.append(e.text)

        for attribute in node.attributes:
            self.visit(attribute)

        for method in node.methods:
            self.visit(method)
            
    @visitor.when(AttributeDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.attribute_type)
        except SemanticError as e:
            self.errors.append(e.text)
            attr_type = ErrorType()
            
        try:
            self.current_type.define_attribute(node.name, attr_type)
        except SemanticError as e:
            self.errors.append(e.text)
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node):
        params_names = []
        params_types = []
        
        for param in node.params:
            if param.lex in params_names:
                self.errors.append(SemanticError(f'Paramenter {param.lex} is already declared.'))
                params_types.append(ErrorType())
                params_names.append(param.lex)
                continue
            
            try:
                param_type = self.context.get_type(param.type)
            except SemanticError as e:
                self.errors.append(e.text)
                param_type = ErrorType()
                
            params_names.append(param.lex)
            params_types.append(param_type)
                
        try:
            return_type = self.context.get_type(node.return_type)
        except SemanticError as e:
            self.errors.append(e.text)
            return_type = ErrorType()

        try:
            self.current_type.define_method(node.name, params_names, params_types, return_type)
        except SemanticError as e:
            self.errors.append(e.text)
