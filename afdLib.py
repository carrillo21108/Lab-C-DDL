from tkinter import SEL
from graphviz import Digraph
from astLib import Node
import afLib
import regexLib
import astLib
import afdLib

class AFDState:
    state_counter = 'A'
    states = set()

    def __init__(self,subset=set()):
        self.name = str(AFDState.state_counter)
        AFDState.state_counter = chr(ord(AFDState.state_counter) + 1)
        AFDState.states.add(self)
        self.subset = subset

        self.transitions = {}
        self.is_accept = False

class AFD:
    def __init__(self):
        self.start = None
        self.accept = set()
        self.states = set()
        self.simulationStates = set()
        
    def step_simulation(self,c,lookAhead):
        if len(self.simulationStates)==0:
            self.simulationStates.add(self.start)

        self.simulationStates = afLib.move(self.simulationStates,c)
            
        return self.simulationStates
        
        
def ast_to_afdd(alphabet,ast_root):
    states = []
    
    afd = AFD()
    states.append(AFDState(subset=ast_root.firstPos))
    afd.start = states[0]
    
    if Node.pos_counter in states[0].subset:
        afd.accept.add(states[0])
        states[0].is_accept = True
    
    contador=0
    nuevosEstados=0
    firstIteration = False
    
    while contador!=nuevosEstados or not firstIteration:
        
        firstIteration=True
        
        if nuevosEstados!=0:
            contador+=1
        
        for symbol in alphabet:
            cambio=False
            subset = set()
            for pos in states[contador].subset:
                if pos in Node.posTable[symbol]:
                    subset=subset.union(Node.followPosTable[pos])
            
            for state in states:
                if state.subset==subset:
                    states[contador].transitions[symbol] = [state]
                    cambio=True
                    break
            
            if cambio!=True and len(subset)>0:
                newState = AFDState(subset)
                
                if Node.pos_counter in subset:
                    afd.accept.add(newState)
                    newState.is_accept = True
                
                states[contador].transitions[symbol] = [newState]
                states.append(newState)
                nuevosEstados+=1
    
    return afd
       
def afn_to_afd(alphabet,afn):
    states = []
    
    So = set()
    So.add(afn.start)
    
    afd = AFD()
    
    states.append(AFDState(subset=afLib.e_closure(So)))
    afd.start = states[0]
    
    if afn.accept in states[0].subset:
        afd.accept.add(states[0])
        states[0].is_accept = True
        

    contador=0
    nuevosEstados=0
    firstIteration = False

    while contador!=nuevosEstados or not firstIteration:
        
        firstIteration=True

        if nuevosEstados!=0:
            contador+=1
        
        for symbol in alphabet:
            cambio=False
            subset=afLib.e_closure(afLib.move(states[contador].subset,symbol))
            
            for state in states:
                if state.subset==subset:
                    states[contador].transitions[symbol] = [state]
                    cambio=True
                    break
            
            if cambio!=True and len(subset)>0:
                newState = AFDState(subset)
                
                if afn.accept in subset:
                    afd.accept.add(newState)
                    newState.is_accept = True
                
                states[contador].transitions[symbol] = [newState]
                states.append(newState)
                nuevosEstados+=1
    
    return afd

def afd_to_afdmin(alphabet, afd):
    #Paso 1 algoritmo
    #Partición conjunto de todos los estados de aceptación y no aceptación (diferencia de conjuntos)
    partition = [afd.states - afd.accept, afd.accept]


    #Paso 2 algoritmo
    while True:
        # Lista vacia para nueva partición de estados.
        partition_new = []
        for G in partition:
            # Para cada grupo de estados en la partición se hacen los subgrupos.
            subgroups = {}
            
            for state in G:
                #Lista de firma de estado
                state_key = []
                
                for c in alphabet:
                    
                    # Revisamos las transiciones del estado para cada símbolo del alfabeto.
                    transition_state = state.transitions.get(c, [])
                    transition_exists = False
                    found_destination_in_s = False
                    
                    for s in partition:
                        for dest_state in transition_state:
                            # Se verifica si el estado de destino está en alguno de los grupos de la partición.
                            if dest_state in s:
                                # Si está, añadimos esa transición a la 'firma' del estado.
                                state_key.append((c, tuple(s)))
                                transition_exists = True
                                found_destination_in_s = True
                                break
                            
                        if found_destination_in_s:
                            break
                        
                    if not transition_exists:
                        # Si no hay transición para este símbolo, añadimos un None a la 'firma'.
                        state_key.append((c, None))
                        
                state_key = tuple(state_key)  # Convertimos la 'firma' a una tupla para poder usarla como clave.
                # Añadimos el estado al subgrupo correspondiente a su 'firma'.
                subgroups.setdefault(state_key, set()).add(state)
                
            partition_new.extend(subgroups.values())
            
        # Si la nueva partición es igual a la anterior, se termina.
        if partition_new == partition:
            break
        else:
            # Si no, actualizamos la partición y lo volvemos a hacer todo de nuevo
            partition = partition_new


    #Paso 3 algoritmo
    #Relacion de estados originales a sus representantes en el AFD minimizado.
    state_relations = {}
    afd_min = AFD()

    for group in partition:
        # Crea un estado que representa todo el grupo, si uno de los estados es de aceptación lo marca asi.
        # Inicializar el estado representativo sin marcarlo como de aceptación por defecto.
        representative = AFDState()
        representative.is_accept = False

        # Ver cada estado para ver si es de aceptacion
        for state in group:
            if state.is_accept:
                representative.is_accept = True
                break  # Si se encuentra un estado de aceptación, ya no importan los demas.

        # agrega el estado representativo
        afd_min.states.add(representative)
        if representative.is_accept:
            #agrega el estado a los estados de aceptación
            afd_min.accept.add(representative)
        for state in group:
            #relaciona el estado original al estado representativo en el AFD minimizado
            state_relations[state] = representative
        if afd.start in group:
            #Si el estado inicial del AFD original, entonces el estado representativo se establece como el estado inicial del AFD minimizado. 
            afd_min.start = representative


    #Paso 4 algoritmo
            
    for old_state, new_state in state_relations.items():
        for c, old_transitions in old_state.transitions.items():
            new_destination_state = state_relations.get(old_transitions[0], None)
            if new_destination_state:
                new_state.transitions[c] = [new_destination_state]

    return afd_min

    
def AFD_simulation(afd,w):
    F = afd.accept
    So = set()
    So.add(afd.start)
    
    S = So
    
    if w!='ε':
        i=0
        while i<len(w):
            c = w[i]
            if c=='ε':
                i+=1
                continue
            if c=='\\' and w[i+1]=='s':
                S = afLib.move(S,' ')
                i+=1
            else:
                S = afLib.move(S,c)
            i+=1
    
    if S:
        s = S.pop()
    else:
        s = None
        
    if s in F:
        return "sí"
    else:
        return "no"
    
def createAFD(item):
    #Construccion de postfix
    postfix = regexLib.shunting_yard(item)
    postfix.append("#")
    postfix.append(".")
            
    #Construccion AST
    ast_root = astLib.create_ast(postfix)
            
    #Construccion AFD
    afd = afdLib.ast_to_afdd(regexLib.regexAlphabet(postfix),ast_root)
    afd.states = afdLib.AFDState.states
    afdLib.AFDState.state_counter = 'A'
    afdLib.AFDState.states = set()
            
    #Minimizacion AFD
    afdmin = afdLib.afd_to_afdmin(regexLib.regexAlphabet(postfix),afd)
    afdmin.states = afdLib.AFDState.states
    afdLib.AFDState.state_counter = 'A'
    afdLib.AFDState.states = set()
    
    return afdmin