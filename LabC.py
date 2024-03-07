from graphviz import Digraph
from yalexLib import YalexRecognizer
import afdLib
import afLib
    
file_path = 'slr-4.yal'

comments = []
definitions = {}
rule = {}

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
    print(content)
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
        print(longer[0])
        #input("Presione [Enter] para continuar.")   
        
    definitions[definition[0]] = definition[1]
    
def ruleRecognize(content):
    # Inicializa la posición
    print(content)
    definition = []
    first = 0
    while first<=len(content):
        #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
        longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
        afdPos = [7,8,9,10,11,3,5,6,0]

        #Revisar entre los AFDs definidos en el yalexRecognizer
        for i in afdPos:
            res = segmentRecognize(i,first,content)
    
            if res[0]:
                print("ACEPTADO por " + str(i))
                print(res[2])
                if len(res[2])>len(longer[2]):
                    longer[0] = i
                    longer[1] = res[1]
                    longer[2] = res[2]
            else:
                print("NO ACEPTADO por " + str(i))
        
        # if longer[0]==3: #ws
        #     pass
        # elif longer[0]==4: #let
        #     pass
        # elif longer[0]==5 and len(definition)==0: #id
        #     definition.append(longer[2])
        # elif longer[0]==6: #eq
        #     pass
        # else: #resto de la definicion
        #     definition.append(content[first:])
        #     break
                
        first = longer[1]
        print(longer[0])
        input("Presione [Enter] para continuar.")   
        
    # definitions[definition[0]] = definition[1]


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
    
print(definitions)

