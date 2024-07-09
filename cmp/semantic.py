import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]
    
    INVALID_NAME = 'The \'%s\' named : \'%s\' already exist in scope.'
    UNDEFINED = 'The \'%s\' named : \'%s\' is not defined.'
    DOUBLE_INHERITANCE = 'The \'%s\' named : \'%s\' already has a parent assigned.'
    WRONG_SIGNATURE = 'Method \'%s\' already defined in an ancestor with a different signature.'
    SELF_IS_READONLY = 'Variable "self" is read-only.'
    INCOMPATIBLE_TYPES = 'Cannot convert \'%s\' into \'%s\'.'
    INVALID_OPERATION = 'Operation \'%s\' is not defined between \'%s\' and \'%s\'.'
    INVALID_UNARY_OPERATION = 'Operation \'%s\' is not defined for \'%s\'.'
    INCONSISTENT_USE = 'Inconsistent use of \'%s\'.'
    EXPECTED_ARGUMENTS = 'Expected %s arguments, but got %s in \'%s\'.'
    CANNOT_INFER_PARAM_TYPE = 'Cannot infer type of parameter \'%s\' in \'%s\'. Please specify it.'
    CANNOT_INFER_ATTR_TYPE = 'Cannot infer type of attribute \'%s\'. Please specify it.'
    CANNOT_INFER_RETURN_TYPE = 'Cannot infer return type of \'%s\'. Please specify it.'
    CANNOT_INFER_VAR_TYPE = 'Cannot infer type of variable \'%s\'. Please specify it.'
    BASE_OUTSIDE_METHOD = 'Cannot use "base" outside of a method.'
    METHOD_NOT_DEFINED = 'Method \'%s\' is not defined in any ancestor.'


class Attribute:
    def __init__(self, name, typex):
        self.name: str = name
        self.type: Type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)
    
    def validate(self):
        errors = []
        if self.type.is_unknow() and not self.type.is_error():
            errors.append(
                SemanticError(SemanticError.CANNOT_INFER_ATTR_TYPE % self.name)
            )
            self.type = ErrorType()
        return errors

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type
        self.param_vars = []

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types
    
    def can_substitute_with(self, other):
        if self.name != other.name:
            return False
        if not other.return_type.conforms_to(self.return_type):
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        for meth_type, impl_type in zip(self.param_types, other.param_types):
            if not meth_type.conforms_to(impl_type):
                return False
        return True
    
    def validate(self):
        errors = []
        for i, param_type in enumerate(self.param_types):
            if param_type.is_unknow() and not param_type.is_error():
                errors.append(
                    SemanticError(
                        SemanticError.CANNOT_INFER_PARAM_TYPE % (self.param_names[i], self.name)
                    )
                )
                self.param_types[i] = ErrorType()

        if self.return_type.is_unknow() and not self.return_type.is_error():
            errors.append(
                SemanticError(SemanticError.CANNOT_INFER_RETURN_TYPE % self.name)
            )
            self.return_type = ErrorType()
        return errors

class Protocol:
    def __init__(self,name:str):
        self.name = name
        self.methods = []
        self.parent = None

    def set_parent(self,parent):
        if self.parent is not None:
            raise SemanticError.DOUBLE_INHERITANCE % ('protocol', self.name)
        self.parent = parent

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            
    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method
    
    def __str__(self):
        output = f'protocol {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.methods else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def bypass(self):
        return False
    
    def is_error(self):
        return False

class ErrorProtocol(Protocol):
    def __init__(self):
        Protocol.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Protocol)
    
    def is_error(self):
        return True


class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.params = []
        self.params_type = []
        self.parent: Type = None
        self.param_vars : list[VariableInfo] = []

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def set_param(self, name:str, type):
        if name in self.params:
            raise SemanticError(f'Param name is already set for {self.name}.')
        self.params.append(name)
        self.params_type.append(type)

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or (self.parent is not None and self.parent.conforms_to(other))

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)
    
    def is_error(self):
        return False
    
    def is_unknow(self) -> bool:
        return False
    
    def validate(self):
        errors = []
        if self.is_error():
            return errors
        
        for attr in self.attributes:
            errors.extend(attr.validate())

        for method in self.methods:
            errors.extend(method.validate())

        for i, param_type in enumerate(self.params_type):
            if param_type.is_unknow():
                errors.append(
                    SemanticError(
                        SemanticError.CANNOT_INFER_PARAM_TYPE % (self.params[i], self.name)
                    )
                )
                self.params_type[i] = ErrorType()
        return errors

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)
    
    def is_error(self):
        return True
    
class UnknowType(Type):
    def __init__(self):
        Type.__init__(self, 'Unknow')
        self.parent = ObjectType()

    def __eq__(self, other:Type):
        return isinstance(other, UnknowType) or other.name == self.name
    
    def is_unknow(self):
        return True
    
    def conforms_to(self, other):
        return True
    

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)
    
class ObjectType(Type):
    def __init__(self):
        super().__init__('Object')

    def __eq__(self, other):
        return isinstance(other, ObjectType) or other.name == self.name

class NumberType(Type):
    def __init__(self):
        Type.__init__(self, 'Number')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, NumberType)
    
class BooleanType(Type):
    def __init__(self):
        Type.__init__(self, 'Boolean')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BooleanType)

class VectorType(Type):
    def __init__(self, type) -> None:
        super().__init__(f'{type.name}[]')
        self.set_parent(ObjectType())
        self.define_method('current', [], [], type)

    def get_element_type(self):
        return self.get_method('current').return_type

    def conforms_to(self, other):
        if not isinstance(other, VectorType):
            return super().conforms_to(other)
        
        self_elem_type = self.get_element_type()
        other_elem_type = other.get_element_type()

        return self_elem_type.conforms_to(other_elem_type)

    def __eq__(self, other):
        return isinstance(other, VectorType) or other.name == self.name
    
class SelfType(Type):
    def __init__(self, referred_type: Type = None) -> None:
        super().__init__('self')
        self.referred_type = referred_type

    def get_attribute(self, name: str) -> Attribute:
        if self.referred_type:
            return self.referred_type.get_attribute(name)

        return super().get_attribute(name)

    def __eq__(self, other):
        return isinstance(other, SelfType) or other.name == self.name

class Context:
    def __init__(self):
        self.types = {}
        self.protocols = {}
        self.parent: Context = None
        self.children = []
        self.functions = {}

    def create_type(self, name:str) -> Type:
        if name in self.types:
            raise SemanticError.INVALID_NAME%('type', name)
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str) -> Type:
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')
        
    def get_type_or_protocol(self, name:str):
        try:
            type_or_protocol = self.get_type(name)
        except SemanticError:
            try:
                type_or_protocol = self.get_protocol(name)
            except SemanticError :
                raise SemanticError(f'Type or protocol "{name}" is not defined.')
        return type_or_protocol
        
    def create_protocol(self, name:str):
        if name in self.protocols:
            raise SemanticError(f'Protocol "{name}" already in context.')
        protocolx = self.protocols[name] = Protocol(name)
        return protocolx
    
    def get_protocol(self, name:str):
        try:
            return self.protocols[name]
        except KeyError:
            raise SemanticError(f'Protocol "{name}" is not defined.')
        
    def create_function(self, name:str, params:list, params_type:list, return_type):
        if name in self.functions:
            raise SemanticError(f'Function "{name}" already in context.')
        functionx = self.functions[name] = Method(name, params, params_type, return_type)
        return functionx
    
    def get_function(self, name:str):
        try:
            return self.functions[name]
        except KeyError:
            raise SemanticError(f'Function "{name}" is not defined.')
        
    
    def create_child_context(self):
        child = Context(self)
        self.children.append(child)


    def __str__(self):
        output = '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'
        output += '{\n\t' + '\n\t'.join(y for x in self.protocols.values() for y in str(x).split('\n')) + '\n}'
        output += '{\n\t' + '\n\t'.join(y for x in self.functions.values() for y in str(x).split('\n')) + '\n}'
        return output

    def __repr__(self):
        return str(self)
    
    def cyclic_type_inheritance(self):
        visited = set()
        visiting = set()
        
        def dfs(node):
            visiting.add(node)
            if node.parent is not None and not node.parent.is_error():
                if node.parent in visiting:
                    return True
                if node.parent not in visited:
                    if dfs(node.parent):
                        return True
            visiting.remove(node)
            visited.add(node)
            return False
        
        for name,type in self.types.items():
            if type not in visited:
                if dfs(type):
                    return True
        
        return False
    
    def cyclic_protocol_inheritance(self):
        visited = set()
        visiting = set()
        
        def dfs(node):
            visiting.add(node)
            if node.parent is not None:
                if node.parent in visiting:
                    return True
                if node.parent not in visited:
                    if dfs(node.parent):
                        return True
            visiting.remove(node)
            visited.add(node)
            return False
        
        for name,protocol in self.protocols.items():
            if protocol not in visited:
                if dfs(protocol):
                    return True
        
        return False
    
    def validate(self):
        errors = []
        for type_name in self.types:
            errors.extend(self.types[type_name].validate())

        for func_name in self.functions:
            errors.extend(self.functions[func_name].validate())

        return errors
    

class VariableInfo:
    def __init__(self, name, vtype, is_param = False):
        self.name: str = name
        self.type: Type = vtype
        self.is_param: bool = is_param
        self.infered_types: list[Type] = []

    def update_type(self, t: Type):
        self.type =  t
        self.infered_types = []

    def infer(self, t: Type):
        self.infered_types.append(t)
    
    def __str__(self):
        return f"[{'param' if self.is_param else 'var'}] {self.name}: {self.type.name};"
    
    def validate(self):

        if self.type.is_unknow() and self.is_param:
            self.type = ErrorType()
            return []

        errors = []
        if self.type.is_unknow() and not self.type.is_error():
            self.type = ErrorType()
            errors.append(
                SemanticError(SemanticError.CANNOT_INFER_VAR_TYPE % self.name)
            )

        return errors

class Scope:
    def __init__(self, parent = None):
        self.locals: list[VariableInfo] = [VariableInfo(name='PI', vtype= NumberType()), VariableInfo(name='E', vtype=NumberType())]
        self.parent: Scope = parent
        self.children: list[Scope] = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)
    
    def __str__(self):
        local = '\n\t'.join(str(x) for x in self.locals)
        children = '\n\t'.join(y for x in self.children for y in str(x).split('\n'))
        children = f"Children: [\n\t {children} \n]\n" if children != '' else ''
        init = '{\n\t' if local != '' or children != '' else '{'
        end = '\n\t}' if local != '' or children != '' else '}'
        middle = '\n\t' if local != '' else ''
        return f'{init}{local}{middle}{children}{end}'

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype, is_param=False):
        info = VariableInfo(vname, vtype, is_param)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        # print("buscando variable ",vname )
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def is_defined(self, vname):
        aux = self.find_variable(vname)
        # print(vname, aux)
        return aux is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
    
    def validate(self):
        errors = []
        for local in self.locals:
            errors.extend(local.validate())

        for child_scope in self.children:
            errors.extend(child_scope.validate())

        return errors
