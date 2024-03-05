
from graphviz import Digraph
import regexLib
import astLib
import afdLib
import afnLib
import afLib
    
file_path = 'slr-1.yal'

delim_regex = "\"\s\t\n\""
ws = f"[{delim_regex}]+"
letter = "'A'-'Z''a'-'z'"
allLetter = f"{letter}\"ÁÉÍÓÚ\"\"áéíóú\""
digit = "'0'-'9'"
_id = f"[{letter}]([{letter}]|[{digit}])*"
especial_chars = "\",_+-.?()|*\""
brackets = "\"\[\]\""
curly_brackets = "\"{}\""
quotes = "'\'''\"'"
backslash = "'\'"

comment_regex = f"\(\*[{allLetter}{digit}{delim_regex}{especial_chars}{brackets}]*\*\)"
definition_regex = f"let{ws}{_id}{ws}={ws}[{letter}{digit}{delim_regex}{especial_chars}{brackets}{quotes}{backslash}]*"
rule_regex = f"rule{ws}tokens{ws}={ws}[{letter}{digit}{delim_regex}{especial_chars}{brackets}{curly_brackets}{quotes}{backslash}"

#Construccion de postfix
postfix = regexLib.shunting_yard(definition_regex)
#Agregando tokens para postfix aumentado
postfix.append("#")
postfix.append(".")

ast_root = astLib.create_ast(postfix)
# tree_graph = astLib.plot_tree(ast_root)
# nombre_archivo_pdf = 'AST'
# tree_graph.view(filename=nombre_archivo_pdf,cleanup=True)

#Construccion AFD
afd = afdLib.ast_to_afdd(regexLib.regexAlphabet(postfix),ast_root)
afd.states = afdLib.AFDState.states
# afd_graph = afLib.plot_af(afd.start)
# nombre_archivo_pdf = 'AFD'
# afd_graph.view(filename=nombre_archivo_pdf,cleanup=True)

#Minimizacion AFD
afdmin = afdLib.afd_to_afdmin(regexLib.regexAlphabet(postfix),afd)
afdmin.states = afdLib.AFDState.states
# afdmin_graph = afLib.plot_af(afdmin.start)
# nombre_archivo_pdf = 'AFD MIN'
# afdmin_graph.view(filename=nombre_archivo_pdf,cleanup=True)

print(afdLib.AFD_simulation(afdmin,"let delim = [\"\s\t\n\"]"))

# with open(file_path, 'r',encoding='utf-8') as file:
#     while True:
#         char = file.read(1)  # Leer un carácter
#         if not char:  # Si char es una cadena vacía, significa que hemos llegado al final del archivo
#             break
#         # Procesa el carácter aquí
#         print(char, end='')