from graphviz import Digraph
from yalexLib import YalexRecognizer
import afdLib
import afLib
    
file_path = 'slr-4.yal'

comments = {}
definitions = {}

def segmentRecognize(afd_pos,i):
    accept = (False,0,"")
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

yalexRecognizer = YalexRecognizer()
# afd_graph = afLib.plot_af(yalexRecognizer.afds[0].start)
# nombre_archivo_pdf = 'AFD'
# afd_graph.view(filename=nombre_archivo_pdf,cleanup=True)

#Lectura del documento yalex
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()  # Leer todo el contenido del archivo
    

# Inicializa la posición
first = 0
while first<=len(content):
    #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
    longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado

    #Revisar entre los AFDs definidos en el yalexRecognizer
    for i in range(0,4):
        res = segmentRecognize(i,first)
    
        if res[0]:
            print("ACEPTADO por " + str(i))
            print(res[2])
            if len(res[2])>len(longer[2]):
                longer[0] = i
                longer[1] = res[1]
                longer[2] = res[2]
        else:
            print("NO ACEPTADO por " + str(i))
            
    first = longer[1]
    input("Presione [Enter] para continuar.")    



