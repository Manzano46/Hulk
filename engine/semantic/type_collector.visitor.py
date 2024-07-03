import cmp.visitor as visitor
from cmp.semantic import SemanticError, Context
from engine.language.ast_nodes import *

# Let's collect the defined types in the AST
class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        self.context = Context()

        object_type = self.context.create_type('Object')

        number_type = self.context.create_type('Number')
        number_type.parent = object_type

        string_type = self.context.create_type('String')
        string_type.parent = object_type

        boolean_type = self.context.create_type('Boolean')
        boolean_type.parent = object_type

        iterable_protocol = self.context.create_protocol('Iterable')
        iterable_protocol.parent = object_type
        
        for declaration in node.declarations:
            self.visit(declaration)
        return self.errors, self.context
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.name)
        except SemanticError as e:
            self.errors.append(e.text)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_protocol(node.idx)
        except SemanticError as e:
            self.errors.append(e.text)
