from cmp.pycompiler import Grammar
from engine.language.ast_nodes import *

G = Grammar()

# Terminals :
    # reserved words
let, printx, func, type_, protocol, extends, is_, as_, concat, concat_sp, in_, if_, elif_, else_, while_, for_, range, new, base, inherits = G.Terminals('let print function type protocol extends is as @ @@ in if elif else while for range new base inherits')
    # symbols
semi, comma, opar, cpar, arrow, colon, semi, opcur, clcur, opcor, clcor, dot, com = G.Terminals('; , ( ) -> : ; { } [ ] . "')

    # operators
equal, plus, minus, star, div, greater, less, mod, pot, or_, andp, not_, equal_equal, not_equal, greater_equal, less_equal, destructive, arrow, pow2, double_or = G.Terminals('= + - * / > < % ^ | & ! == != >= <= := => ** ||')

    # 
idx, num, string, boolean = G.Terminals('id number string boolean')


# NonTerminals :
    #start symbol
program = G.NonTerminal('<program>', startSymbol=True)

global_expression, special_exp, expression, declarations, decl = G.NonTerminals('<global_expression> <special_exp> <expression> <declarations> <decl>')

let_exp, if_exp, loop_exp, assignment_exp = G.NonTerminals('<let_exp> <if_exp> <loop_exp> <assignment_exp>')

expr, block, term, factor = G.NonTerminals('<expr> <block> <term> <factor>')

func_decl, meth, params, param, body, type_decl, protocol_decl, expr_list, comp_exp,var_exp = G.NonTerminals('<func-decl> <meth> <params> <param> <body> <type_decl> <protocol_decl> <expr-list> <comp_exp> <var_exp>')

feature_list, feature, assignment, assignment_list, func_call, args, pro_meths, pro_meth, id_id_list, is_as_exp, concat_exp, pow_exp, type_exp, not_exp = G.NonTerminals('<feature_list> <feature> <assignment> <assignment_list> <func_call> <args> <pro_meths> <pro_meth> <id_id_list> <is_as_exp> <concat_exp> <pow_exp> <type_exp> <not_exp>')

boolean_exp, arithmetic_exp, vector_exp, atomic_exp, elif_exp = G.NonTerminals('<boolean_exp> <arithmetic_exp> <vector_exp> <atomic_exp> <elif_exp>')

# Productions
program %= global_expression, lambda h,s : ProgramNode([],s[1])
program %= declarations + global_expression, lambda h,s : ProgramNode(s[1], s[2])

global_expression %= special_exp, lambda h, s : s[1]
global_expression %= expression, lambda h, s : s[1]

declarations %= declarations + decl, lambda h, s: s[1] + [s[2]]
declarations %= decl, lambda h, s: [s[1]]

decl %= func_decl, lambda h,s : s[1]
decl %= protocol_decl, lambda h,s : s[1]
decl %= type_decl, lambda h,s : s[1]

special_exp %= let_exp, lambda h,s : s[1] # special_expression -> let_expression
special_exp %= if_exp, lambda h,s : s[1] #                      | if_expression
special_exp %= loop_exp, lambda h,s : s[1] #                    | loop_expresion (while or for)
special_exp %= assignment_exp, lambda h,s : s[1]  #             | assignment_expression 

expression %= expr + semi, lambda h, s: s[1] # expression -> a special_expression or a block with semicolon at the end
expression %= block, lambda h, s: s[1] #                   | a block without semicolon at the end , couse its optional

expr %= block, lambda h,s : s[1] # expression -> { expression; expression; ...}
expr %= special_exp, lambda h,s : s[1] #       | special_expression

block %= opcur + expr_list + clcur, lambda h,s : ExpressionBlockNode(s[2]) # block -> { expression; expression ...}

expr_list %= expression + expr_list, lambda h, s: [s[1]] + s[2]  # expression_list -> expression; expression; ...
expr_list %= expression, lambda h, s: [s[1]] #                               | expression;

body %= arrow + special_exp + semi, lambda h,s : s[2] # body -> => expression ;
body %= block, lambda h,s : s[1] #                            | { block }

args %= expr, lambda h,s : [s[1]] #                     args -> expression
args %= expr + comma + args, lambda h,s : [s[1]] + s[3] #     | expression , expression ...

assignment_exp %= boolean_exp + destructive + assignment_exp , lambda h,s : DestructiveAssignmentNode(s[1], s[3]) # assignment_expression -> boolean_expression := assignment_expression
assignment_exp %= boolean_exp, lambda h,s : s[1] #                                                                                         | boolean_exp

boolean_exp %= boolean_exp + or_  + comp_exp, lambda h,s : OrNode(s[1], s[3]) # boolean_expression -> boolean_expression | comparation_expression
boolean_exp %= boolean_exp + andp + comp_exp, lambda h,s : AndNode(s[1], s[3]) #                    |boolean_expression & comparation_expression
boolean_exp %= comp_exp, lambda h,s : s[1] #                                                        |comparation_expression

comp_exp %= comp_exp + equal_equal + is_as_exp, lambda h,s : EqualNode(s[1], s[3]) # comparation_expression -> comparation_expresion == comparation_expression
comp_exp %= comp_exp + not_equal + is_as_exp, lambda h,s : NotEqualNode(s[1], s[3]) #                        | comparation_expression != comparation_expression
comp_exp %= comp_exp + greater + is_as_exp, lambda h,s : GreaterThanNode(s[1], s[3]) #                       | comparation_expression > comparation_expression
comp_exp %= comp_exp + less + is_as_exp, lambda h,s : LessThanNode(s[1], s[3]) #                             | comparation_expression < comparation_expression
comp_exp %= comp_exp + greater_equal + is_as_exp, lambda h,s : GreaterOrEqualNode(s[1], s[3]) #              | comparation_expression >= comparation_expression
comp_exp %= comp_exp + less_equal + is_as_exp,lambda h,s : LessOrEqualNode(s[1], s[3]) #                     | comparation_expression <= comparation_expression
comp_exp %= is_as_exp, lambda h,s : s[1] #                                                                   | is_as_expression

is_as_exp %= is_as_exp + is_ + idx, lambda h,s : IsNode(s[1], s[3]) # is/as_expression -> is/as_expression is type
is_as_exp %= is_as_exp + as_ + idx, lambda h,s : AsNode(s[1], s[3]) #                   | is/as_expression as type
is_as_exp %= concat_exp, lambda h,s : s[1] #                                            | concatenation_expression

concat_exp %= concat_exp + concat + arithmetic_exp, lambda h,s : ConcatNode(s[1], s[3], s[2]) # concatenation_expression -> concatenation_expression @ arithmetic_expression
concat_exp %= concat_exp + concat_sp + arithmetic_exp, lambda h,s : ConcatNode(s[1], s[3], s[2]) #                        | concatenation_expression @@ arithmetic_expression
concat_exp %= arithmetic_exp, lambda h,s : s[1] #                                                                         | arithmetic_expression

arithmetic_exp %= arithmetic_exp + plus + term, lambda h,s : PlusNode(s[1], s[3]) # arithmetic_expression -> arithmetic_expression + term
arithmetic_exp %= arithmetic_exp + minus + term, lambda h,s : MinusNode(s[1], s[3]) #                      | arithmetic_expression - term
arithmetic_exp %= term, lambda h,s : s[1] #                                                                | term

term %= term + star + factor, lambda h,s : StarNode(s[1], s[3]) # term -> term * factor
term %= term + div + factor, lambda h,s : DivNode(s[1], s[3]) #         | term / factor
term %= term + mod + factor, lambda h,s : ModNode(s[1], s[3]) #         | term % factor
term %= factor, lambda h,s : s[1] #                                     | factor

factor %= minus + pow_exp, lambda h,s : NegNode(s[2]) # factor -> - pow_operation
factor %= pow_exp, lambda h,s : s[1] #                          | pow_operation

pow_exp %= type_exp + pow2 + pow_exp, lambda h,s : PowNode(s[1], s[3]) # pow_expression -> pow_expression ** type_expression
pow_exp %= type_exp + pot + pow_exp, lambda h,s : PowNode(s[1], s[3]) #                  | pow_expression ^ type_expression
pow_exp %= type_exp, lambda h,s : s[1] #                                                 | type_expression

type_exp %= new + idx + opar + cpar, lambda h,s : TypeInstantiationNode(s[2],[]) # type_expression -> new type ( )
type_exp %= new + idx + opar + args + cpar, lambda h,s : TypeInstantiationNode(s[2], s[4]) #        | new type ( arg , arg ...)
type_exp %= not_exp, lambda h,s : s[1] #                                                            | not_expression

not_exp %= not_ + var_exp, lambda h,s : NotNode(s[2]) # not_expression -> ! var_expression
not_exp %= var_exp, lambda h,s : s[1] #                                 | var_expression

var_exp %= var_exp + dot + idx + opar + cpar, lambda h,s : MethodCallNode(s[1],s[3],[]) # var_expression -> object.method ()
var_exp %= var_exp + dot + idx + opar + args + cpar, lambda h,s : MethodCallNode(s[1],s[3],s[5]) #        | object.method (arg, arg ...)
var_exp %= var_exp + dot + idx, lambda h,s : AttributeCallNode(s[1],s[3]) #                               | object.attribute
var_exp %= var_exp + opcor + expr + clcor, lambda h,s : IndexingNode(s[1], s[3])  #                       | name [expression]
var_exp %= opar + expr + cpar, lambda h,s : s[2]        #                                                 | (expression)
var_exp %= atomic_exp, lambda h,s : s[1] #                                                                | atomic_expression

atomic_exp %= num, lambda h,s : NumberNode(s[1]) #    atomic_expression -> number
atomic_exp %= boolean, lambda h,s : BooleanNode(s[1]) #                  | boolean
atomic_exp %= string, lambda h,s : StringNode(s[1]) #                    | string
atomic_exp %= idx, lambda h,s : VariableNode(s[1]) #                     | name
atomic_exp %= func_call, lambda h,s : s[1] #                             | func_call
atomic_exp %= vector_exp, lambda h,s : s[1] #                            | vector_expression
atomic_exp %= base + opar + cpar, lambda h,s : BaseCallNode([]) #        | base  ()
atomic_exp %= base + opar + args + cpar, lambda h,s : BaseCallNode(s[3])#| base (expression,expression...)

func_call %= idx + opar + cpar, lambda h,s : FunctionCallNode(s[1],[]) # | function_call -> name ()
func_call %= idx + opar + args + cpar, lambda h,s : FunctionCallNode(s[1], s[3]) #        | name (expression, expression...)

vector_exp %= opcor + args + clcor, lambda h,s : VectorInitializationNode(s[2]) #                     vector_expression -> [expression, expression ...]
vector_exp %= opcor + expr + double_or + idx + in_ + expr + clcor, lambda h,s : VectorComprehensionNode(s[2],s[4],s[6]) # | [expression || id in expression]

assignment %= idx + equal + expr, lambda h,s : VarDeclarationNode(s[1],s[3]) #           assignment -> name = expression
assignment %= idx + colon + idx + equal + expr, lambda h,s : VarDeclarationNode(s[1],s[5],s[3]) #    | name : type = expression

feature_list %= feature, lambda h,s : [s[1]] #                feature_list -> feature
feature_list %= feature + feature_list, lambda h,s : [s[1]] + s[2] #        | feature feature ...

feature %= assignment + semi, lambda h,s : s[1] # feature -> assignment ;
feature %= meth, lambda h,s : s[1] #                       | method

# Functions and methods ----------------------------------------------------------------
func_decl %= func + idx + opar + params + cpar + body, lambda h,s : FunctionDeclarationNode(s[2], s[4], s[6]) # function_declaration -> function name (params) body
func_decl %= func + idx + opar + params + cpar + colon + idx + body, lambda h,s : FunctionDeclarationNode(s[2], s[4], s[8], s[7]) #            | function name (params) return_type body

meth %= idx + opar + params + cpar + body, lambda h,s : MethodDeclarationNode(s[1], s[3], s[5]) # method_declaration -> name (params) body
meth %= idx + opar + params + cpar + colon + idx + body, lambda h,s : MethodDeclarationNode(s[1], s[3], s[6], s[5]) #         | name (params) : return_type body

params %= param, lambda h,s : [s[1]] #                      params -> param
params %= param + comma + params, lambda h,s : [s[1]] + s[3] #      | param , param ....
params %= G.Epsilon, lambda h,s : []

param %= idx, lambda h,s : VariableNode(s[1]) #                 param -> name
param %= idx + colon + idx, lambda h,s : VariableNode(s[1],s[3]) #     | name : type

# Types ----------------------------------------------------------------
type_decl %= type_ + idx + opcur + feature_list + clcur, lambda h,s : TypeDeclarationNode(s[2], [], s[4]) # type_declaration -> type name { assignments and methods}
type_decl %= type_ + idx + opar + params + cpar + opcur + feature_list + clcur, lambda h,s : TypeDeclarationNode(s[2], s[4], s[7]) # type_declaration -> type name (params) { assignments and methods}
type_decl %= type_ + idx + inherits + idx + opcur + feature_list + clcur, lambda h,s : TypeDeclarationNode(s[2], [], s[6], s[4]) # type_declaration -> type name inherits name { assignments and methods}
type_decl %= type_ + idx + inherits + idx + opar + args + cpar + opcur + feature_list + clcur, lambda h,s : TypeDeclarationNode(s[2], [], s[8], s[4], s[6]) # type_declaration -> type name inherits name (args) { assignments and methods}
type_decl %= type_ + idx + opar + params + cpar + inherits + idx + opcur + feature_list + clcur, lambda h,s : TypeDeclarationNode(s[2], s[4], s[9], s[7]) # type_declaration -> type name (params) inherits name { assignments and methods}
type_decl %= type_ + idx + opar + params + cpar + inherits + idx + opar + args + cpar + opcur + feature_list + clcur, lambda h,s : TypeDeclarationNode(s[2], s[4], s[12], s[7], s[9]) # type_declaration -> type name (params) inherits name (args) { assignments and methods}

# Protocoles
protocol_decl %= protocol + idx + opcur + clcur, lambda h,s : ProtocolDeclarationNode(s[2]) #                                  protocol -> protocol name {}
protocol_decl %= protocol + idx + opcur + pro_meths + clcur, lambda h,s : ProtocolDeclarationNode(s[2], s[4]) #                          | protocol name {meth meth ...}
protocol_decl %= protocol + idx + extends + idx + opcur + pro_meths + clcur, lambda h,s : ProtocolDeclarationNode(s[2], s[6], s[4]) #    | protocol name extends name {meth meth ...}

pro_meths %= pro_meth, lambda h,s : [s[1]] #                     pro_meths -> pro_meth
pro_meths %= pro_meth + semi + pro_meths, lambda h,s : [s[1]] + s[2] #      | pro_meth ; pro_meth ...

pro_meth %= idx + opar + cpar + colon + idx, lambda h,s : MethodSignatureDeclarationNode(s[1], [], s[5]) #            pro_meth -> name () : type
pro_meth %= idx + opar + id_id_list + cpar + colon + idx, lambda h,s : MethodSignatureDeclarationNode(s[1], s[3], s[6]) #       | name ( name : type, name : type , ...) : type

id_id_list %= idx + colon + idx, lambda h,s : [VariableNode(s[1], s[3])] #                 id_id_list -> name : type
id_id_list %= idx + colon + idx + comma + id_id_list, lambda h,s : [VariableNode(s[1], s[3])] + s[5] # | name : type, name : type , ...

# Let in ------------------------------------------------------------------------------------
let_exp %= let + assignment_list + in_ + expr, lambda h,s : LetInNode(s[2], s[4]) # let_expression -> let var = expression, var = expression ... in expression

assignment_list %= assignment, lambda h,s : [s[1]] #         assignment_list -> var = expression
assignment_list %= assignment + comma + assignment_list, lambda h,s : [s[1]] + s[3] # | var = expression, var = expression ...

# Conditional --------------------------------------------------------------------------------
if_exp %= if_ + opar + expr + cpar + expr + else_ + expr, lambda h,s : ConditionalNode([(s[3],s[5])], s[7]) #             if_exp -> if (expression) expression else expression
if_exp %= if_ + opar + expr + cpar + expr + elif_exp + else_ + expr, lambda h,s : ConditionalNode([(s[3],s[5])] + s[6], s[8]) #   | if (expression) expression elif ...  else expression
elif_exp %= elif_ + opar + expr + cpar + expr, lambda h,s : [(s[3],s[5])] #     elif_expression -> elif (expression) expression
elif_exp %= elif_ + opar + expr + cpar + expr + elif_exp, lambda h,s : ([(s[3],s[5])] + s[6]) #  | elif (expression) expression elif ...

# Loop ---------------------------------------------------------------------------------------
loop_exp %= while_ + opar + expr + cpar + expr, lambda h,s : WhileNode(s[3], s[5]) # loop expression -> while (boolean_exp) expression
loop_exp %= for_ + opar + idx + in_ + expr + cpar + expr, lambda h,s : ForNode(s[3], s[5], s[7]) #    | for id in expression expression
