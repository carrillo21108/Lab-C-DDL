from graphviz import Digraph
from yalexLib import YalexRecognizer
import afdLib
import afLib
    
file_path = 'slr-4.yal'

comments = []
definitions = {}
rule_tokens = {}

definitions_id = []
tokens_regex = []

def segmentRecognize(afd_pos,i,content):
    accept = (False,0,"")
    first = i
    # Bucle hasta que se alcance el final del contenido
    while i <= len(content):  # Asegura que haya espacio para lookAhead
        char = content[i] if i<len(content) else ""  # Carácter actual
        lookAhead = content[i + 1] if i<len(content)-1 else ""  # Carácter siguiente
        
        # Procesa el carácter aquí
        res =yalexRecognizer.step_simulate_AFD(afd_pos, char, lookAhead)
        if res == 0:
            last = i+1
            accept = (True,last,content[first:last]) #Estado de aceptacion, ultima posicion de lookAhead, contenido aceptado
        
        elif res == 2:
            if accept[0]:
                return accept
            else:
                return (False,0,"")

        i += 1  # Incrementa la posición para el próximo carácter
        
def definitionRecognize(content):
    # Inicializa la posición
    #print(content)
    definition = []
    first = 0
    while first<=len(content):
        #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
        longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
        afdPos = [3,4,5,6]

        #Revisar entre los AFDs definidos en el yalexRecognizer
        for i in afdPos:
            res = segmentRecognize(i,first,content)
    
            if res[0]:
                # print("ACEPTADO por " + str(i))
                # print(res[2])
                if len(res[2])>len(longer[2]):
                    longer[0] = i
                    longer[1] = res[1]
                    longer[2] = res[2]
            # else:
            #     print("NO ACEPTADO por " + str(i))
        
        if longer[0]==3: #ws
            pass
        elif longer[0]==4: #let
            pass
        elif longer[0]==5 and len(definition)==0: #id
            definition.append(longer[2])
        elif longer[0]==6: #eq
            pass
        else: #resto de la definicion
            definition.append(content[first:])
            break
                
        first = longer[1]
        #print(longer[0])
        #input("Presione [Enter] para continuar.")   
        
    definitions[definition[0]] = definition[1]
    
def ruleRecognize(content):
    # Inicializa la posición
    #print(content)
    identifier = []
    first = 0
    while first<=len(content):
        #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
        longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
        afdPos = [7,8,9,10,11,3,5,6,0]

        #Revisar entre los AFDs definidos en el yalexRecognizer
        for i in afdPos:
            res = segmentRecognize(i,first,content)
    
            if res[0]:
                # print("ACEPTADO por " + str(i))
                # print(res[2])
                if len(res[2])>len(longer[2]):
                    longer[0] = i
                    longer[1] = res[1]
                    longer[2] = res[2]
            # else:
            #     print("NO ACEPTADO por " + str(i))
        
        if longer[0]==7: #rule
            pass
        elif longer[0]==8: #tokens
            pass
        elif longer[0]==9: #char o string
            identifier.append(longer[2])
        elif longer[0]==10: #|
            pass
        elif longer[0]==11: #{return SOMETHING}
            rule_tokens[identifier.pop()] = longer[2]
        elif longer[0]==3: #ws
            pass
        elif longer[0]==5: #id
            identifier.append(longer[2])
        elif longer[0]==6: #eq
            pass
        elif longer[0]==0: #Comentario
            comments.append(longer[2])
        else: #resto de la definicion
            break
                
        first = longer[1]
        #print(longer[0])
        #input("Presione [Enter] para continuar.")
        
    for item in identifier:
        rule_tokens[item] = ""

def valueRecognize(content):
    # Inicializa la posición
    # print(content)
    new_content = ""
    first = 0
    change = True
    while change:
        while first<=len(content):
            #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
            longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
            afdPos = new_afdPos

            #Revisar entre los AFDs definidos en el yalexRecognizer
            for i in afdPos:
                res = segmentRecognize(i,first,content)
    
                if res[0]:
                    # print("ACEPTADO por " + str(i))
                    # print(res[2])
                    if len(res[2])>len(longer[2]):
                        longer[0] = i
                        longer[1] = res[1]
                        longer[2] = res[2]
                # else:
                #     print("NO ACEPTADO por " + str(i))
        
            if longer[0]==12:
                new_content+=longer[2]
                first = longer[1]
                
            elif longer[0]!=-1:
                new_content+=definitions[longer[2]]
                first = longer[1]
            else:
                new_content+=content[first] if first<len(content) else ""
                first+=1
            
            # print(longer[0])
            # input("Presione [Enter] para continuar.")
        
        if content!=new_content:
            first=0
            content=new_content
            new_content=""
            # print("CONTENIDO: "+content)
        else:
            change = False
            # print("CONTENIDO: "+content)
            
    return new_content
        
yalexRecognizer = YalexRecognizer()
# afd_graph = afLib.plot_af(yalexRecognizer.afds[0].start)
# nombre_archivo_pdf = 'AFD'
# afd_graph.view(filename=nombre_archivo_pdf,cleanup=True)

#Lectura del documento yalex
with open(file_path, 'r', encoding='utf-8') as file:
    yalexContent = file.read()  # Leer todo el contenido del archivo
    

# Inicializa la posición
first = 0
while first<=len(yalexContent):
    #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
    longer = [-1,len(yalexContent)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
    afdPos = [0,1,2,3]

    #Revisar entre los AFDs definidos en el yalexRecognizer
    for i in afdPos:
        res = segmentRecognize(i,first,yalexContent)
    
        if res[0]:
            # print("ACEPTADO por " + str(i))
            # print(res[2])
            if len(res[2])>len(longer[2]):
                longer[0] = i
                longer[1] = res[1]
                longer[2] = res[2]
        # else:
        #     print("NO ACEPTADO por " + str(i))
    
    if longer[0]==0: #Comentario
        comments.append(longer[2])
    elif longer[0]==1: #Definicion
        definitionRecognize(longer[2])
    elif longer[0]==2: #Rule
        ruleRecognize(longer[2])
    elif longer[0]==3: #ws
        pass
    elif longer[0]==-1 and first!=len(yalexContent): #Error
        print("ERROR al reconocer archivo Yalex")
        break

    first = longer[1]
    #input("Presione [Enter] para continuar.")
    
print(comments)
print('\n')
print(definitions)
print('\n')
print(rule_tokens)
print('\n')

for key in rule_tokens:
    tokens_regex.append(key)

for key in definitions:
    definitions_id.append(key)
    

new_afdPos = [12]
i=12
for item in definitions_id:
    yalexRecognizer.afds.append(afdLib.createAFD(item))
    i+=1
    new_afdPos.append(i)

i=0

print(tokens_regex)
print('\n')
while i<len(tokens_regex):
    tokens_regex[i] = valueRecognize(tokens_regex[i])
    i+=1

print(tokens_regex)
    