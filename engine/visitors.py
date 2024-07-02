import cmp.visitor as visitor
from cmp.semantic import *
from engine.language.ast_nodes import *

############-------------Funciones-----------------##################
# Todas las funciones deben estar definidas antes de la expresion global final, todas viven en un espacio de 
# nombres global
# No importa el orden de la definicion de funciones para usarlas dentro de otras
# Todas las funciones tienen valor de retorno

###########------------Variables--------------------##################
# Una expresion let siempre tiene un valor de retorno
# Una variable puede ocultar otra con el mismo nombre si esta definida en un scoupe interior o en el mismo 
# Una variable asignada destructivamente devueve el valor recien asignado

###########------------Tipos--------------------##############
# La palabra base dentro de un metodo se refiere a la implementacion del metodo que tenga el mismo nombre del 
# ancestro mas cercano
# A todos los atributos se les debe dar una expresion de inicializacion
# La palabra self no es un objetivo de asignacion valido
# No se pueden usar atributos de un tipo en las expresiones de inicializacion de otro atributo de ese mismo tipo
# No se hereda de los tipos incorporados (num,str,bool)

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
        self.context.types = {'int' : IntType(), 'void' : VoidType()}
        
        for declaration in node.declarations:
            self.visit(declaration)
        return self.errors, self.context
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.name)
        except SemanticError as e:
            self.errors.append(e.text)


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


# Let's check if the types are correctly used
