import cmp.visitor as visitor


class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []

class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.vars = {}
        self.constants = {}

class ParamNode(Node):
    def __init__(self, name):
        self.name = name

class LocalNode(Node):
    def __init__(self, name):
        self.name = name

class InstructionNode(Node):
    pass

class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class PowNode(ArithmeticNode):
    pass

class ModNode(ArithmeticNode):
    pass

class GetAttribNode(InstructionNode):
    def __init__(self, obj, attribute, dest):
        self.obj = obj
        self.attribute = attribute
        self.dest = dest

class SetAttribNode(InstructionNode):
    def __init__(self, obj, attribute, value):
        self.obj = obj
        self.attribute = attribute
        self.value = value

class GetIndexNode(InstructionNode):
    pass

class SetIndexNode(InstructionNode):
    pass

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

class ArrayNode(InstructionNode):
    pass

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label

class GotoIfNode(InstructionNode):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest):
        self.type = xtype
        self.method = method
        self.dest = dest

class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

class LengthNode(InstructionNode):
    pass

class ConcatNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PrefixNode(InstructionNode):
    pass

class SubstringNode(InstructionNode):
    pass

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr
    
class NotNode(InstructionNode):
    def __inti__(self, dest, value):
        self.value = value
        self.dest = dest


class NegNode(InstructionNode):
    def __inti__(self, dest, value):
        self.value = value
        self.dest = dest

class OrNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest


class AndNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest


class LessThanNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest


class GreaterThanNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest


class LessOrEqualNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest


class GreaterOrEqualNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest

class EqualNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest


class NotEqualNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.left = left
        self.right = right
        self.dest = dest



def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(DataNode)
        def visit(self, node : DataNode):
            return f'{node.name}  = {node.value}'
        

        @visitor.when(TypeNode)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(FunctionNode)
        def visit(self, node):
            #print(node.instructions)
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            #print(node.instructions , 'fffffffffffffffffffffffffffffffffffffffffffff')
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(ParamNode)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node):
            return f'{node.dest} = {node.source}'
        
        @visitor.when(NotNode)
        def visit(self, node : NotNode):
            return f'{node.dest} = !{node.value}'
        
        @visitor.when(NegNode)
        def visit(self, node : NegNode):
            return f'{node.dest} = -{node.value}'

        @visitor.when(ConcatNode)
        def visit(self, node : ConcatNode):
            return f'{node.dest} = CONCAT {node.left} {node.right}'

        @visitor.when(PlusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} + {node.right}'

        @visitor.when(MinusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} - {node.right}'

        @visitor.when(StarNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} * {node.right}'

        @visitor.when(ModNode)
        def visit(self, node : ModNode):
            return f'{node.dest} = {node.left} % {node.right}'
        
        @visitor.when(PowNode)
        def visit(self, node : PowNode):
            return f'{node.dest} = {node.left} ^ {node.right}'

        @visitor.when(DivNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} / {node.right}'
        
        @visitor.when(OrNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} | {node.right}'
        
        @visitor.when(AndNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} & {node.right}'
        
        @visitor.when(GreaterOrEqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} >= {node.right}'

        @visitor.when(GreaterThanNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} > {node.right}'

        @visitor.when(LessOrEqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} <= {node.right}'
        
        @visitor.when(LessThanNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} < {node.right}'
        
        @visitor.when(NotEqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} != {node.right}'
        
        @visitor.when(EqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} == {node.right}'
        
        @visitor.when(AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.type}'

        @visitor.when(StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgNode)
        def visit(self, node):
            return f'ARG {node.name}'

        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'

        @visitor.when(PrintNode)
        def visit(self, node):
            return f'PRINT {node.str_addr if node.str_addr is not None else ""}'
        
        @visitor.when(LoadNode)
        def visit(self, node):
            return f'{node.dest} = LOAD {node.msg}'
        
        @visitor.when(LabelNode)
        def visit(self, node):
            return f'LABEL {node.name}'
        
        @visitor.when(GotoNode)
        def visit(self, node):
            return f'GOTO {node.label}'
        
        @visitor.when(GotoIfNode)
        def visit(self, node : GotoIfNode):
            return f'IF {node.condition} GOTO {node.label}'
        
        @visitor.when(DynamicCallNode)
        def visit(self, node : DynamicCallNode):
            return f'{node.dest} =  VCALL {node.type} {node.method}'
        
        @visitor.when(SetAttribNode)
        def visit(self, node : SetAttribNode):
            return f'SETATTR {node.obj} {node.attribute} {node.value}'
        
        @visitor.when(GetAttribNode)
        def visit(self, node : GetAttribNode):
            return f'{node.dest} = GETATTR {node.obj} {node.attribute}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))