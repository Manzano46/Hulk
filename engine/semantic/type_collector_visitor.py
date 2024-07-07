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

        self.context.types['Unknown'] = UnknowType()

        object_type = self.context.create_type('Object')

        number_type = self.context.create_type('Number')
        number_type.parent = object_type

        boolean_type = self.context.create_type('Boolean')
        boolean_type.parent = object_type
        
        string_type = self.context.create_type('String')
        string_type.parent = object_type
        string_type.define_method('size', [], [], number_type)
        string_type.define_method('next', [], [], boolean_type)
        string_type.define_method('current', [], [], string_type)

        object_type.define_method('equals', ['other'], [object_type], boolean_type)
        object_type.define_method('toString', [], [], string_type)

        self.context.create_function('print', ['value'], [object_type], string_type)
        self.context.create_function('sqrt', ['value'], [number_type], number_type)
        self.context.create_function('sin', ['angle'], [number_type], number_type)
        self.context.create_function('cos', ['angle'], [number_type], number_type)
        self.context.create_function('exp', ['value'], [number_type], number_type)
        self.context.create_function('log', ['value'], [number_type], number_type)
        self.context.create_function('rand', [], [], number_type)

        range_type = self.context.create_type('Range')
        range_type.set_parent(object_type)
        range_type.params_names, range_type.params_types = ['min', 'max'], [number_type, number_type]
        range_type.define_attribute('min', number_type)
        range_type.define_attribute('max', number_type)
        range_type.define_attribute('current', number_type)
        range_type.define_method('next', [], [], boolean_type)
        range_type.define_method('current', [], [], number_type)

        self.context.create_function('range', ['min', 'max'], [number_type, number_type], range_type)

        iterable_protocol = self.context.create_protocol('Iterable')
        iterable_protocol.parent = object_type
        iterable_protocol.define_method('next', [], [], boolean_type)
        iterable_protocol.define_method('current', [], [], object_type)

        for declaration in node.declarations:
            self.visit(declaration)
        return self.errors, self.context
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.name)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_protocol(node.idx)
        except SemanticError as e:
            self.errors.append(e)
