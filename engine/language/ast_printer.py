import cmp.visitor as visitor
from engine.language.ast_nodes import *

def get_ast_printer():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node, tabs=0):
            return ''.join(self.visit(declaration, tabs) for declaration in node.declarations + [node.expression])
        
        @visitor.when(UnaryExpressionNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.operand, tabs + 1)
            return f'{ans}\n{child}'

        @visitor.when(BinaryExpressionNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(AtomicNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

        @visitor.when(FunctionDeclarationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            params = ''.join('\n' + self.visit(param, tabs + 1) for param in node.params)
            child = self.visit(node.expr, tabs + 1)
            return f'{ans}\n{params}\n{child}'

        @visitor.when(MethodDeclarationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            params = ''.join('\n' + self.visit(param, tabs + 1) for param in node.params)
            child = self.visit(node.expr, tabs + 1)
            return f'{ans}\n{params}\n{child}'
        
        @visitor.when(MethodSignatureDeclarationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            params = ''.join('\n' + self.visit(param, tabs + 1) for param in node.params)
            
            return f'{ans}\n{params}'
        
        @visitor.when(AttributeDeclarationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.expr, tabs + 1)
            return f'{ans}\n{child}'
        
        @visitor.when(TypeDeclarationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            params = ''.join('\n' + self.visit(param, tabs + 1) for param in node.params)
            body = ''.join('\n' + self.visit(feature, tabs + 1) for feature in node.body)
            return f'{ans}\n{params}\n{body}'
        
        @visitor.when(ProtocolDeclarationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.method_signature, tabs + 1)
            
            return f'{ans}\n{child}'
        
        @visitor.when(VarDeclarationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.expr, tabs + 1)
            
            return f'{ans}\n{child}'
        
        @visitor.when(LetInNode)
        def visit(self, node : LetInNode, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            declarations = ''.join('\n' + self.visit(declaration, tabs + 1) for declaration in node.var_declarations)
            
            child = self.visit(node.expr, tabs + 1)
            return f'{ans}\n{declarations}\n{child}'
        
        @visitor.when(ConditionalNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            conditions = ''.join('\n' + self.visit(condition, tabs + 1) for condition in node.condition_expression_list)
            
            child = self.visit(node.else_expr, tabs + 1)
            
            return f'{ans}\n{conditions}\n{child}'
        
        @visitor.when(WhileNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            condition = self.visit(node.condition, tabs + 1)
           
            child = self.visit(node.expression, tabs + 1)
            
            return f'{ans}\n{condition}\n{child}'
        
        @visitor.when(ForNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
           
            child = self.visit(node.expression, tabs + 1)
            
            return f'{ans}\n{child}'
        
        @visitor.when(ExpressionBlockNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            expressions = ''.join('\n' + self.visit(expression, tabs + 1) for expression in node.expressions)
            
            return f'{ans}\n{expressions}'
        
        @visitor.when(DestructiveAssignmentNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
           
            child = self.visit(node.expr, tabs + 1)
            
            return f'{ans}\n{child}'
        
        @visitor.when(IsNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
           
            child = self.visit(node.expression, tabs + 1)
            
            return f'{ans}\n{child}'
        
        @visitor.when(AsNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
           
            child = self.visit(node.expression, tabs + 1)
            
            return f'{ans}\n{child}'
        
        @visitor.when(FunctionCallNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            args = ''.join('\n' + self.visit(arg, tabs + 1) for arg in node.args)
            
            return f'{ans}\n{args}'
        
        @visitor.when(IndexingNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
           
            child = self.visit(node.index, tabs + 1)
            
            return f'{ans}\n{child}'
        
        @visitor.when(TypeInstantiationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            args = ''.join('\n' + self.visit(arg, tabs + 1) for arg in node.args)
            
            return f'{ans}\n{args}'
        
        @visitor.when(AttributeCallNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            
            return f'{ans}'
        
        @visitor.when(VectorInitializationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            args = ''.join('\n' + self.visit(arg, tabs + 1) for arg in node.elements)
            
            return f'{ans}\n{args}'
        
        @visitor.when(VectorComprehensionNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
           
            return f'{ans}'
        
        @visitor.when(MethodCallNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            args = ''.join('\n' + self.visit(arg, tabs + 1) for arg in node.args)
            
            return f'{ans}\n{args}'
        
        @visitor.when(BaseCallNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            args = ''.join('\n' + self.visit(arg, tabs + 1) for arg in node.args)
            
            return f'{ans}\n{args}'
        
        @visitor.when(PrintNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.expr, tabs + 1)
            
            return f'{ans}\n{child}'
        
        

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))