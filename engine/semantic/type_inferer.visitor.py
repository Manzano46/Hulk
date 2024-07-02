import cmp.visitor as visitor
from cmp.semantic import SemanticError, Context, ErrorType
from engine.language.ast_nodes import *

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
        self.current_type = self.context.get_type(node.name)

        if self.current_type.is_error():
            return
        
        parent_args_types = [self.visit(arg) for arg in node.parent_args]
        #to be continued ....




    @visitor.when(AttributeDeclarationNode)
    def visit(self, node):
        inf_type = self.visit(node.expr)

        attribute = self.current_type.get_attribute(node.id)

        if attribute.type.is_error():
            attr_type = ErrorType()
        elif attribute.type != types.AutoType():
            attr_type = attribute.type
        else:
            attr_type = inf_type

        attribute.type = attr_type
        return attr_type
