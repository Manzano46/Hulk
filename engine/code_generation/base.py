import cmp.cil as cil
from cmp.semantic import Scope, VariableInfo
from cmp.semantic import Context

class BaseHulkToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context : Context = context
        self.main = None
        self.labels = 0
        self.vself = VariableInfo('self', None)
        self.value_types = ['String', 'Int', 'Bool']
    
    @property
    def params(self):
        if self.current_function != None:
            return self.current_function.params
        else:
            return self.main.params
    
    @property
    def localvars(self):
        if self.current_function != None:
            return self.current_function.localvars
        else:
            return self.main.localvars
    
    @property
    def instructions(self):
        if self.current_function != None:
            return self.current_function.instructions
        else:
            return self.main.instructions
        
    @property
    def function(self):
        if self.current_function != None:
            return self.current_function
        else:
            return self.main
    
    def find(self, name):
        #print(self.function.vars)
        if self.current_type is not None:
            #print(self.current_type.attributes)
            for attribute in self.current_type.attributes:
                if attribute.name == name:
                    return attribute.name 
        if name in self.function.vars:
            return self.function.vars[name]
        return None        
        
    def register_local(self, vinfo):
        name = vinfo.name
        vinfo.name = f'local_{self.function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        self.function.vars[name] = vinfo.name
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)
    
    def register_param(self, vinfo):
        if vinfo is None:
            return None
        name = vinfo.name
        vinfo.name = f'param_{self.function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node = cil.ParamNode(vinfo.name)
        self.params.append(param_node)
        self.function.vars[name] = vinfo.name
        return vinfo.name

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node
    
    def find_cte(self, value):
        for key, xvalue in self.function.constants:
            if xvalue == value:
                return key
        return None
        
    def register_local_cte(self, value):
        name = f'local_{self.function.name[9:]}_constant_{len(self.function.constants)}'
        local_node = cil.LocalNode(name)
        self.localvars.append(local_node)
        self.function.vars[name] = value
        return name