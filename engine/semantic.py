import cmp.visitor as visitor
from cmp.semantic import SemanticError
from engine.language.ast_nodes import *
from context import *

############-------------Funciones-----------------##################
# Todas las funciones deben estar definidas antes de la expresion global final, todas viven en un espacio de 
# nombres global
# No importa el orden de la definicion de funciones para usarlas dentro de otras
# Todas las funciones tienen valor de retorno

###########------------Variables--------------------##################
# Una expresion let siempre tiene un valor de retorno
# Una variable puede ocultar otra con el mismo nombre si esta definida en un scoupe interior o en el mismo 
# Una variable asignada destructivamente devueve el valor recien asignado

###########------------Tipos--------------------##############
# La palabra base dentro de un metodo se refiere a la implementacion del metodo que tenga el mismo nombre del 
# ancestro mas cercano
# A todos los atributos se les debe dar una expresion de inicializacion
# La palabra self no es un objetivo de asignacion valido
# No se pueden usar atributos de un tipo en las expresiones de inicializacion de otro atributo de ese mismo tipo
# No se hereda de los tipos incorporados (num,str,bool)




