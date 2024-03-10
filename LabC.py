from graphviz import Digraph
from yalexLib import YalexRecognizer
import afdLib
import afLib
import astLib
import regexLib
    
file_path = 'slr-4.yal'

definitions_id = []
tokens_regex = []
        
yalexRecognizer = YalexRecognizer()

#Lectura del documento yalex
with open(file_path, 'r', encoding='utf-8') as file:
    yalexContent = file.read()  # Leer todo el contenido del archivo
    
if yalexRecognizer.yalexRecognize(yalexContent):
    print(yalexRecognizer.get_comments())
    print('\n')
    print(yalexRecognizer.get_definitions())
    print('\n')
    print(yalexRecognizer.get_rule_tokens())
    print('\n')
    

    for key in yalexRecognizer.get_rule_tokens():
        tokens_regex.append(key)

    for key in yalexRecognizer.get_definitions():
        definitions_id.append(key)
    

    new_afdPos = [12] #Reconociendo chars y strings
    i=12
    for item in definitions_id:
        yalexRecognizer.afds.append(afdLib.createAFD(item))
        i+=1
        new_afdPos.append(i)

    i=0

    print(tokens_regex)
    print('\n')
    #Reemplazando las variables de las definiciones en el regex de tokens
    while i<len(tokens_regex):
        tokens_regex[i] = yalexRecognizer.valueRecognize(new_afdPos,tokens_regex[i])
        i+=1

    print(tokens_regex)
    print('\n')

    k=1
    for item in tokens_regex:
        # subafd = afdLib.createAFD(item)
        # subafd_graph = afLib.plot_af(subafd.start)
        # nombre_archivo_pdf = 'AFD '+str(k)
        # subafd_graph.view(filename=nombre_archivo_pdf,cleanup=True)
        postfix = regexLib.shunting_yard(item)
            
        #Construccion AST
        ast_root = astLib.create_ast(postfix)
        ast_graph = astLib.plot_tree(ast_root)
        nombre_archivo_pdf = 'Subarbol de Expresion '+str(k)
        ast_graph.view(filename=nombre_archivo_pdf,cleanup=True)
        k+=1

    lexer = '|'.join(tokens_regex)
    lexer = '('+lexer+')'

    print(lexer)
    print('\n')
    #Construccion de postfix
    postfix = regexLib.shunting_yard(lexer)
            
    #Construccion AST
    ast_root = astLib.create_ast(postfix)
    ast_graph = astLib.plot_tree(ast_root)
    nombre_archivo_pdf = 'Arbol de expresion'
    ast_graph.view(filename=nombre_archivo_pdf,cleanup=True)