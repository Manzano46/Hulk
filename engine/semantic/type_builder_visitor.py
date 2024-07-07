
import cmp.visitor as visitor
from cmp.semantic import *
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

        # if self.context.cyclic_type_inheritance():
        #     self.errors.append(SemanticError('There is cyclic inheritance of types'))

        # if self.context.cyclic_protocol_inheritance():
        #     self.errors.append(SemanticError('There is cyclic inheritance of protocols'))

        return self.errors, self.context

    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        print('visitando el tipo ' + node.name)
        try:
            self.current_type = self.context.get_type(node.name)
        except SemanticError as e:
            self.errors.append(e)
            self.current_type = ErrorType()

        if node.parent != None:
            try:
                current_parent_type = self.context.get_type(node.parent)
            except SemanticError as e:
                self.errors.append(e)
                current_parent_type = ErrorType()
            try:
                self.current_type.set_parent(current_parent_type)
            except SemanticError as e:
                self.errors.append(e)

        for attribute in node.attributes:
            self.visit(attribute)

        for method in node.methods:
            self.visit(method)
            
    @visitor.when(AttributeDeclarationNode)
    def visit(self, node):
        if node.attribute_type is None:
            attr_type = UnknowType()
        else:
            try:
                attr_type = self.context.get_type_or_protocol(node.attribute_type)
            except SemanticError as e:
                self.errors.append(e)
                attr_type = ErrorType()
            
        try:
            self.current_type.define_attribute(node.name, attr_type)
        except SemanticError as e:
            self.errors.append(e)
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node):
        params_names = []
        params_types = []
        
        for param in node.params:
            if param.lex in params_names:
                self.errors.append(SemanticError(SemanticError.INVALID_NAME%('parameter', param.lex)))
                params_types.append(ErrorType())
                params_names.append(param.lex)
                continue
            if param.type is None :
                param_type = UnknowType()
            else:
                try:
                    param_type = self.context.get_type_or_protocol(param.type)
                except SemanticError as e:
                    self.errors.append(e)
                    param_type = ErrorType()
                
            params_names.append(param.lex)
            params_types.append(param_type)

        if node.return_type is None:
            return_type = UnknowType() 
        else : 
            try:
                return_type = self.context.get_type_or_protocol(node.return_type)
            except SemanticError as e:
                self.errors.append(e)
                return_type = ErrorType()

        try:
            self.current_type.define_method(node.name, params_names, params_types, return_type)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node):
        try:
            self.current_protocol = self.context.get_protocol(node.idx)
        except SemanticError as e:
            self.errors.append(e)
            self.current_protocol = ErrorProtocol()

        if node.parent != None:
            try:
                current_parent_protocol = self.context.get_protocol(node.parent)
            except SemanticError as e:
                self.errors.append(e)
                current_parent_protocol = ErrorProtocol()
            try:
                self.current_protocol.set_parent(current_parent_protocol)
            except SemanticError as e:
                self.errors.append(e)

        for method in node.methods_signature:
            self.visit(method)

    @visitor.when(MethodSignatureDeclarationNode)
    def visit(self, node):
        params_names = []
        params_types = []
        
        for param in node.params:
            if param.lex in params_names:
                self.errors.append(SemanticError(SemanticError.INVALID_NAME%('parameter', param.lex)))
                params_types.append(ErrorProtocol())
                params_names.append(param.lex)
                continue
            
            try:
                param_type = self.context.get_type_or_protocol(param.type)
            except SemanticError as e:
                self.errors.append(e)
                param_type = ErrorType()
                
            params_names.append(param.lex)
            params_types.append(param_type)
                
        try:
            return_type = self.context.get_type_or_protocol(node.return_type)
        except SemanticError as e:
            self.errors.append(e)
            return_type = ErrorType()

        try:
            self.current_protocol.define_method(node.name, params_names, params_types, return_type)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node):
        params = []
        params_type = []
        for param in node.params:
            params.append(param.lex)
            if param.type is None : 
                params_type.append(UnknowType())
            else : 
                try:
                    param_type = self.context.get_type_or_protocol(param.type)
                except SemanticError as e:
                    param_type = ErrorType()
                    self.errors.append(e)
                params_type.append(param_type)

        if node.return_type is None:
            return_type = UnknowType()
        else:
            try:
                return_type = self.context.get_type_or_protocol(node.return_type)
            except SemanticError as e:
                self.errors.append(e)
                return_type = ErrorType()

        try:
            self.context.create_function(node.id, params, params_type, return_type)
        except SemanticError as e:
            self.errors.append(e)
    

            

