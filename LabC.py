
from graphviz import Digraph
import regexLib
import astLib
import afdLib
import afnLib
import afLib
    
file_path = 'slr-1.yal'

#comment_postfix = "\(\*([A-Z]|[a-z]| |[0-9])*\*\)"
comment_regex = "a+?"
#Construccion de postfix
postfix = regexLib.shunting_yard(comment_regex)

print(f"Expresion regular: {comment_regex}")
print(f"Postfijo: {postfix}")
#Agregando tokens para postfix aumentado
postfix.append("#")
postfix.append(".")

ast_root = astLib.create_ast(postfix)
tree_graph = astLib.plot_tree(ast_root)
nombre_archivo_pdf = 'AST'
tree_graph.view(filename=nombre_archivo_pdf,cleanup=True)

afd = afdLib.ast_to_afdd(regexLib.regexAlphabet(postfix),ast_root)
afd.states = afdLib.AFDState.states

afd_graph = afLib.plot_af(afd.start)
nombre_archivo_pdf = 'AFD'
afd_graph.view(filename=nombre_archivo_pdf,cleanup=True)

# with open(file_path, 'r',encoding='utf-8') as file:
#     while True:
#         char = file.read(1)  # Leer un carácter
#         if not char:  # Si char es una cadena vacía, significa que hemos llegado al final del archivo
#             break
#         # Procesa el carácter aquí
#         print(char, end='')