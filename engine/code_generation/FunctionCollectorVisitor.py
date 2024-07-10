from cmp.cil import *

class FunctionCollectorVisitor:
    def __init__(self):
        self.function_count = 0
        self.functions = {}

    def generate_function_name(self):
        self.function_count += 1
        return f"Function_{self.function_count}"

    @visitor.on("node")
    def collect(self, node):
        pass

    @visitor.when(ProgramNode)
    def collect(self, node: ProgramNode):
        for func in node.dotcode:
            self.collect(func)

    @visitor.when(FunctionNode)
    def collect(self, node: FunctionNode):
        if node.name == "entry":
            self.functions[node.name] = "main"
        else:
            self.functions[node.name] = self.generate_function_name()