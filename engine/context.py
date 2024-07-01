from ast import *
     

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
        self.parent = parent
        self.children = []
        self.types = {}
    
    def get_type(self, name:str):
        return self.types[name]
    
    def create_child_context(self):
        child = Context(self)
        self.children.append(child)

    def create_type(self, name:str):
        new_type = TypeInfo(self, name)
        self.types[name] = new_type

