import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name: str = name
        self.type: Type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types


class Protocol:
    def __init__(self,name:str):
        self.name = name
        self.methods = []
        self.parent = None

    def set_parent(self,parent):
        if self.parent is not None:
            raise SemanticError(f'Parent protocol is already set for {self.name}.')
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

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

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
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

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
        Type.__init__(self, '<unknow>')

    def __eq__(self, other):
        return isinstance(other, UnknowType) or other.name == self.name
    
    def is_unknow(self):
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

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)
    
class BooleanType(Type):
    def __init__(self):
        Type.__init__(self, 'bool')

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

class Context:
    def __init__(self):
        self.types = {}
        self.protocols = {}
        self.parent: Context = None
        self.children = []
        self.functions = {}
     
    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')
        
    def get_type_or_protocol(self, name:str):
        try:
            type_or_protocol = self.get_type(name)
        except :
            try:
                type_or_protocol = self.get_protocol(name)
            except SemanticError as e:
                self.errors.append(e.text)
                type_or_protocol = ErrorType()
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
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
