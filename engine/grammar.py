from cmp.pycompiler import Grammar
G = Grammar()

program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat, decl = G.NonTerminals('<stat_list> <stat> <decl>')
def_func, print_stat = G.NonTerminals('<def-func> <print-stat>')
expr, term, factor = G.NonTerminals('<expr> <term> <factor>')
func_decl, meth, params, param, body, block, type_decl, protocol_decl, expr_list, comp_exp = G.NonTerminals('<func-decl> <meth> <params> <param> <body> <block> <type_decl> <protocol_decl> <expr-list> <comp_exp>')
feature_list, feature, assignment, assignment_list, var, inherits, args, pro_meths, pro_meth, id_id_list = G.NonTerminals('<feature_list> <feature> <assignment> <assignment_list> <var> <inherits> <args> <pro_meths> <pro_meth> <id_id_list>')
let_exp, if_exp, loop_exp, boolean_exp, arithmetic_exp, assignment_exp, vector_exp, atomic_exp, rest_if = G.NonTerminals('<let_exp> <if_exp> <loop_exp> <boolean_exp> <arithmetic_exp> <assignment_exp> <vector_exp> <atomic_exp> <rest_if>')

let, printx, func, type_, protocol, extends, is_, as_, concat, in_, if_, elif_, else_, while_, for_, range, new = G.Terminals('let print function type protocol extends is as @@ in if elif else while for range new')
semi, comma, opar, cpar, arrow, colon, semi, opcur, clcur, opcor, clcor, dot, com = G.Terminals('; , ( ) -> : ; { } [ ] . "')
or_, andp, not_ = G.Terminals('| & !')
equal, plus, minus, star, div, greater, less, mod, pot = G.Terminals('= + - * / > < % ^')
idx, num, string, boolean = G.Terminals('id int string boolean')

program %= stat_list

stat_list %= stat + semi # statement_list -> statement ,
stat_list %= stat + semi + stat_list # statment_list -> statement , statement ...

stat %= decl # statement -> declaration
stat %= expr #            | expression

decl %= func_decl # declaration -> function_declaration
decl %= type_decl #               |type_declaration
decl %= protocol_decl #           |protocol_declaration

func_decl %= func + meth # function_declaration -> function method

meth %= idx + opar + params + cpar + body # method_declaration -> name (params) body
meth %= idx + opar + params + cpar + idx + body # method_declaration -> name (params) return_type body

params %= param # params -> param
params %= param + comma + params # params -> param , param ....

param %= idx # param -> name
param %= idx + colon + idx # param -> name : type
param %= G.Epsilon 

body %= equal + greater + expr + semi # body -> => expression ;
body %= block # body -> { block }

block %= opcur + expr_list + clcur # block +> { expression; expression ...}

type_decl %= type_ + idx + opcur + feature_list + clcur # type_declaration -> type name { assignments and methods}
type_decl %= type_ + idx + opar + params + opcur + feature_list + clcur # type_declaration -> type name (params) { assignments and methods}
type_decl %= type_ + idx + inherits + idx + opcur + feature_list + clcur # type_declaration -> type name inherits name { assignments and methods}
type_decl %= type_ + idx + inherits + opar + args + cpar + opcur + feature_list + clcur # type_declaration -> type name inherits name (args) { assignments and methods}
type_decl %= type_ + idx + opar + params + cpar + inherits + idx + opcur + feature_list + clcur # type_declaration -> type name (params) inherits name { assignments and methods}
type_decl %= type_ + idx + opar + params + cpar + inherits + idx + opar + args + cpar + opcur + feature_list + clcur # type_declaration -> type name (params) inherits name (args) { assignments and methods}

args %= expr # args -> expression
args %= expr + comma + args # args -> expression , expression ...

assignment %= idx + equal + expr # assignment -> name = expression
assignment %= idx + colon + idx + equal + expr # assignment -> name : type = expression

feature_list %= feature # feature_list -> feature
feature_list %= feature + feature_list # feature_list -> feature feature ...

feature %= assignment + semi # feature -> assignment ;
feature %= meth # feature -> method

protocol_decl %= protocol + idx + opcur + clcur # protocol -> protocol name {}
protocol_decl %= protocol + idx + opcur + pro_meths + clcur # protocol -> protocol name {meth meth ...}
protocol_decl %= protocol + idx + extends + idx + opcur + pro_meths + clcur # protocol -> protocol name {meth meth ...}

pro_meths %= pro_meth # pro_meths -> pro_meth
pro_meths %= pro_meth + semi + pro_meths # pro_meths -> pro_meth ; pro_meth ...

pro_meth %= idx + opar + cpar + colon + idx # pro_meth -> name () : type
pro_meth %= idx + opar + id_id_list + cpar + colon + idx # pro_meth -> name ( name : type, name : type , ...) : type

id_id_list %= idx + colon + idx # id_id_list -> name : type
id_id_list %= idx + colon + idx + comma + id_id_list # id_id_list -> name : type, name : type , ...

expr %= let_exp
expr %= if_exp
expr %= loop_exp
expr %= block
expr %= boolean_exp
expr %= expr + is_ + idx
expr %= expr + concat + expr
expr %= arithmetic_exp
expr %= expr + as_ + idx
expr %= assignment_exp
expr %= vector_exp
expr %= atomic_exp

let_exp %= let + assignment_list + in_ + expr

assignment_list %= assignment
assignment_list %= assignment + assignment_list

if_exp %= if_ + opar + boolean_exp + cpar + expr + rest_if # if_exp -> if (boolean_exp) expression elif ... elif else expression
rest_if %= elif_ + opar + expr + cpar + expr + rest_if # rest_if -> elif (expression) expression elif ...
rest_if %= else_ + expr # rest_if -> else expression

loop_exp %= while_ + opar + boolean_exp + cpar + expr # loop expression -> while (boolean_exp) expression
loop_exp %= for_ + idx + in_ + range + opar + expr + comma +  expr + cpar + expr # for id in range(exp,exp) expression

boolean_exp %= boolean_exp + or_ + or_ + comp_exp
boolean_exp %= boolean_exp + andp + andp + comp_exp
boolean_exp %= boolean_exp + equal + equal + comp_exp
boolean_exp %= not_ + comp_exp
boolean_exp %= comp_exp
boolean_exp %= boolean

comp_exp %= arithmetic_exp + greater + arithmetic_exp
comp_exp %= arithmetic_exp + less + arithmetic_exp
comp_exp %= arithmetic_exp + greater + equal + arithmetic_exp
comp_exp %= arithmetic_exp + less + equal + arithmetic_exp
comp_exp %= arithmetic_exp

arithmetic_exp %= arithmetic_exp + plus + term
arithmetic_exp %= arithmetic_exp + minus + term
arithmetic_exp %= minus + term
arithmetic_exp %= term

term %= term + star + factor
term %= term + div + factor
term %= term + mod + factor
term %= factor

factor %= factor + star + star + atomic_exp
factor %= factor + pot + atomic_exp
factor %= atomic_exp

assignment_exp %= var + colon + equal + expr # assignment_expression -> variable := expression

var %= var + opcor + expr + clcor # variable -> name[expression]
var %= var + dot + var # variable -> name.attribute
var %= idx # variable -> name

vector_exp %= opcor + clcor # vector -> [ ]
vector_exp %= opcor + args + clcor # vector -> [expression, expression ...]
vector_exp %= opcor + expr + or_ + or_ + expr + in_ + expr + clcor # vector -> [expression || expression in expression]

atomic_exp %= new + idx + opar + cpar # atomic_expression -> new type ( )
atomic_exp %= new + idx + opar + args + cpar # atomic_expression -> new type ( arg , arg ...)
atomic_exp %= num
atomic_exp %= com + string + com
atomic_exp %= boolean
atomic_exp %= var + opar + cpar # atomic_expression -> name ()
atomic_exp %= var + opar + args + cpar # atomic_expression -> name (arg, arg ...)
atomic_exp %= opar + expr + cpar # atomic_expression -> ( expression )



print_stat %= printx + expr # Your code here!!! (add rule)

print(G)