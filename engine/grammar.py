from cmp.pycompiler import Grammar
from ast_nodes import *
G = Grammar()

# Terminals :
    # reserved words
let, printx, func, type_, protocol, extends, is_, as_, concat, concat_sp, in_, if_, elif_, else_, while_, for_, range, new, base = G.Terminals('let print function type protocol extends is as @ @@ in if elif else while for range new base')
    # symbols
semi, comma, opar, cpar, arrow, colon, semi, opcur, clcur, opcor, clcor, dot, com = G.Terminals('; , ( ) -> : ; { } [ ] . "')

    # operators
equal, plus, minus, star, div, greater, less, mod, pot, or_, andp, not_ = G.Terminals('= + - * / > < % ^ | & !')

    # 
idx, num, string, boolean = G.Terminals('id int string boolean')


# NonTerminals :
    #start symbol
program = G.NonTerminal('<program>', startSymbol=True)

stat_list, stat, decl, special_exp = G.NonTerminals('<stat_list> <stat> <decl> <special_exp>')

def_func, print_stat = G.NonTerminals('<def-func> <print-stat>')

expr, term, factor = G.NonTerminals('<expr> <term> <factor>')

func_decl, meth, params, param, body, block, type_decl, protocol_decl, expr_list, comp_exp,var_exp = G.NonTerminals('<func-decl> <meth> <params> <param> <body> <block> <type_decl> <protocol_decl> <expr-list> <comp_exp> <var_exp>')

feature_list, feature, assignment, assignment_list, var, inherits, args, pro_meths, pro_meth, id_id_list, is_as_exp, concat_exp, pow_exp, type_exp, not_exp = G.NonTerminals('<feature_list> <feature> <assignment> <assignment_list> <var> <inherits> <args> <pro_meths> <pro_meth> <id_id_list> <is_as_exp> <concat_exp> <pow_exp> <type_exp> <not_exp>')

let_exp, if_exp, loop_exp, boolean_exp, arithmetic_exp, assignment_exp, vector_exp, atomic_exp, rest_if = G.NonTerminals('<let_exp> <if_exp> <loop_exp> <boolean_exp> <arithmetic_exp> <assignment_exp> <vector_exp> <atomic_exp> <rest_if>')

# Productions

program %= stat_list, lambda h,s : ProgramNode(s[1])  # program -> statement_list

stat_list %= stat, lambda h,s : StatementNode(s[1])  # statement_list -> statement ,
stat_list %= stat + stat_list  # statment_list -> statement , statement ...

stat %= special_exp # statement -> special expression
stat %= expr + semi #            | expression ;
stat %= block #                  | {expression; expression...} 
stat %= decl  #                  | declaration

expr %= block # expression -> { expression; expression; ...}
expr %= special_exp #       | special_expression

special_exp %= let_exp #             | let_expression
special_exp %= if_exp #              | if_expression
special_exp %= loop_exp #            | loop_expresion (while or for)
special_exp %= assignment_exp  #     | assignment_expression 

block %= opcur + expr_list + clcur # block -> { expression; expression ...}

body %= equal + greater + expr + semi # body -> => expression ;
body %= block # body -> { block }

args %= expr # args -> expression
args %= expr + comma + args # args -> expression , expression ...

assignment_exp %= var + colon + equal + boolean_exp # assignment_expression -> variable := expression
assignment_exp %= boolean_exp #                                              |boolean_exp

boolean_exp %= boolean_exp + or_ + or_ + comp_exp # boolean_expression -> boolean_expression || comparation_expression
boolean_exp %= boolean_exp + andp + andp + comp_exp #                    |boolean_expression && comparation_expression
boolean_exp %= comp_exp #                                                |comparation_expression

comp_exp %= comp_exp + equal + equal + is_as_exp # comparation_expression -> comparation_expresion == comparation_expression
comp_exp %= comp_exp + not_ + equal + is_as_exp #                          |comparation_expression != comparation_expression
comp_exp %= comp_exp + greater + is_as_exp #                               |comparation_expression > comparation_expression
comp_exp %= comp_exp + less + is_as_exp #                                  |comparation_expression < comparation_expression
comp_exp %= comp_exp + greater + equal + is_as_exp #                       |comparation_expression >= comparation_expression
comp_exp %= comp_exp + less + equal + is_as_exp #                          |comparation_expression <= comparation_expression
comp_exp %= is_as_exp #                                                    |is_as_expression

is_as_exp %= is_as_exp + is_ + idx # is/as_expression -> is/as_expression is type
is_as_exp %= is_as_exp + as_ + idx #                   | is/as_expression as type
is_as_exp %= concat_exp #                              |concatenation_expression

concat_exp %= concat_exp + concat + arithmetic_exp # concatenation_expression -> concatenation_expression @ arithmetic_expression
concat_exp %= concat_exp + concat_sp + arithmetic_exp #                        | concatenation_expression @@ arithmetic_expression
concat_exp %= arithmetic_exp #                                                 | arithmetic_expression

arithmetic_exp %= arithmetic_exp + plus + term # arithmetic_expression -> arithmetic_expression + term
arithmetic_exp %= arithmetic_exp + minus + term #                       | arithmetic_expression - term
arithmetic_exp %= term #                                                | term

term %= term + star + factor # term -> term * factor
term %= term + div + factor #        | term / factor
term %= term + mod + factor #        | term % factor
term %= factor #                     | factor

factor %= minus + pow_exp # factor -> - pow_operation
factor %= pow_exp #                 | pow_operation

pow_exp %= pow_exp + star + star + type_exp # pow_expression -> pow_expression ** type_expression
pow_exp %= pow_exp + pot + type_exp #                         | pow_expression ^ type_expression
pow_exp %= type_exp #                                         | type_expression

type_exp %= new + idx + opar + cpar # type_expression -> new type ( )
type_exp %= new + idx + opar + args + cpar #           | new type ( arg , arg ...)
type_exp %= not_exp #                                  | not_expression

not_exp %= not_ + var_exp # not_expression -> ! var_expression
not_exp %= var_exp #                        | var_expression

var_exp %= var + opar + cpar # var_expression -> name ()
var_exp %= var + opar + args + cpar #          | name (arg, arg ...)
var_exp %= atomic_exp #                        | atomic_expression

var %= var + opcor + expr + clcor # variable -> name[expression]
var %= var + dot + var # variable -> name.attribute
var %= idx # variable -> name

atomic_exp %= opar + expr + cpar # atomic_expression -> (expression)
atomic_exp %= num #                                   | number
atomic_exp %= boolean #                               | boolean
atomic_exp %= string #                                | string
atomic_exp %= var #                                   | name.attribute
atomic_exp %= vector_exp #                            | vector_expression
atomic_exp %= base + opar + cpar #                    | base  ()
atomic_exp %= base + opar + args + cpar #             | base (expression,expression...)

vector_exp %= idx + opcor + clcor # vector -> type [ ]
vector_exp %= opcor + args + clcor #        | [expression, expression ...]
vector_exp %= opcor + expr + or_ + or_ + idx + in_ + expr + clcor # vector -> [expression || id in expression]

assignment %= idx + equal + expr # assignment -> name = expression
assignment %= idx + colon + idx + equal + expr # assignment -> name : type = expression

feature_list %= feature # feature_list -> feature
feature_list %= feature + feature_list # feature_list -> feature feature ...

feature %= assignment + semi # feature -> assignment ;
feature %= meth # feature -> method


# Declarations of functions, types and methods-----------------------------------------------------------------------------
decl %= func_decl # declaration -> function_declaration
decl %= type_decl #               |type_declaration
decl %= protocol_decl #           |protocol_declaration

# Functions and methods ----------------------------------------------------------------
func_decl %= func + meth # function_declaration -> function method

meth %= idx + opar + params + cpar + body # method_declaration -> name (params) body
meth %= idx + opar + params + cpar + idx + body #               | name (params) return_type body

params %= param # params -> param
params %= param + comma + params # params -> param , param ....

param %= idx # param -> name
param %= idx + colon + idx # param -> name : type
param %= G.Epsilon 

# Types ----------------------------------------------------------------
type_decl %= type_ + idx + opcur + feature_list + clcur # type_declaration -> type name { assignments and methods}
type_decl %= type_ + idx + opar + params + opcur + feature_list + clcur # type_declaration -> type name (params) { assignments and methods}
type_decl %= type_ + idx + inherits + idx + opcur + feature_list + clcur # type_declaration -> type name inherits name { assignments and methods}
type_decl %= type_ + idx + inherits + opar + args + cpar + opcur + feature_list + clcur # type_declaration -> type name inherits name (args) { assignments and methods}
type_decl %= type_ + idx + opar + params + cpar + inherits + idx + opcur + feature_list + clcur # type_declaration -> type name (params) inherits name { assignments and methods}
type_decl %= type_ + idx + opar + params + cpar + inherits + idx + opar + args + cpar + opcur + feature_list + clcur # type_declaration -> type name (params) inherits name (args) { assignments and methods}

# Protocoles
protocol_decl %= protocol + idx + opcur + clcur # protocol -> protocol name {}
protocol_decl %= protocol + idx + opcur + pro_meths + clcur # protocol -> protocol name {meth meth ...}
protocol_decl %= protocol + idx + extends + idx + opcur + pro_meths + clcur # protocol -> protocol name {meth meth ...}

pro_meths %= pro_meth # pro_meths -> pro_meth
pro_meths %= pro_meth + semi + pro_meths # pro_meths -> pro_meth ; pro_meth ...

pro_meth %= idx + opar + cpar + colon + idx # pro_meth -> name () : type
pro_meth %= idx + opar + id_id_list + cpar + colon + idx # pro_meth -> name ( name : type, name : type , ...) : type

id_id_list %= idx + colon + idx # id_id_list -> name : type
id_id_list %= idx + colon + idx + comma + id_id_list # id_id_list -> name : type, name : type , ...

# Let in ------------------------------------------------------------------------------------
let_exp %= let + assignment_list + in_ + expr

assignment_list %= assignment
assignment_list %= assignment + assignment_list

# Conditional --------------------------------------------------------------------------------
if_exp %= if_ + opar + boolean_exp + cpar + expr + rest_if # if_exp -> if (boolean_exp) expression elif ... elif else expression
rest_if %= elif_ + opar + expr + cpar + expr + rest_if # rest_if -> elif (expression) expression elif ...
rest_if %= else_ + expr # rest_if -> else expression

# Loop ---------------------------------------------------------------------------------------
loop_exp %= while_ + opar + boolean_exp + cpar + expr # loop expression -> while (boolean_exp) expression
loop_exp %= for_ + idx + in_ + range + opar + expr + comma +  expr + cpar + expr # for id in range(exp,exp) expression



print_stat %= printx + expr # Your code here!!! (add rule)

print(G)