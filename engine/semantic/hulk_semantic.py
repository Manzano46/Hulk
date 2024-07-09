from engine.semantic.type_builder_visitor import TypeBuilder
from engine.semantic.type_checker_visitor import TypeChecker
from engine.semantic.type_collector_visitor import TypeCollector
from engine.semantic.type_inferer_visitor import TypeInferer
from engine.semantic.variable_collector_visitor import VarCollector
from engine.semantic.ast_printer import get_ast_printer

def semantic_analysis_pipeline(ast, debug=False):
    if debug:
        print('===================== AST =====================')
        printer = get_ast_printer()
        print(printer(ast))

    if debug:
        print('============== COLLECTING TYPES ===============')

    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('=============== BUILDING TYPES ================')

    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('=============== CHECKING TYPES ================')
        print('---------------- COLLECTING VARIABLES ------------------')

    var_collector = VarCollector(context, errors)
    scope = var_collector.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
        print('---------------- INFERRING TYPES ------------------')

    type_inferrer = TypeInferer(context, errors)
    type_inferrer.visit(ast)
    inference_errors = context.validate() + scope.validate()
    errors.extend(inference_errors)

    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
        print('---------------- CHECKING TYPES ------------------')
    type_checker = TypeChecker(context, errors)
    type_checker.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
        
    return ast, errors, context, scope
