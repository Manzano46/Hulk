from ast import *
from cmp.semantic import SemanticError

class TypeInfo :
    def __init__(self,name):
        self.name = name
        self.attributes = {}
        self.methods = {}
        self.parent = None

    def define_attribute(self,name:str, type):
        if name in self.attributes.keys():
            return False
        self.attributes[name] = AttributeInfo(name,type)
        return True

    def define_method(self,name:str, return_type, arguments):
        if name in self.methods.keys():
            return False
        self.methods[name] = MethodInfo(name, return_type, arguments)
        return True
    
    def get_attribute(self,name):
        return self.attributes[name]
    
    def get_method(self,name):
        return self.methods[name]
    
    def set_parent(self, parent):
        self.parent = parent

    def is_error(self):
        return False

class ErrorType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)
    
    def is_error(self):
        return True

class AttributeInfo :
    def __init__(self,name:str, type: TypeInfo):
        self.name = name
        self.type = type



class MethodInfo:
    def __init__(self,name:str, return_type:TypeInfo, arguments):
        self.name = name
        self.return_type = return_type
        self.arguments = arguments


class Context(object):
    def __init__(self, parent):
        self.parent: Context = parent
        self.children = []
        self.types = {}
    
    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f"Type {name} is not defined.")
    
    def create_child_context(self):
        child = Context(self)
        self.children.append(child)

    def create_type(self, name:str):
        new_type = TypeInfo(self, name)
        self.types[name] = new_type

class Scope:
    def __init__(self, parent=None):
        self.parent: Scope = parent
        self.children = []
        self.locals = []
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