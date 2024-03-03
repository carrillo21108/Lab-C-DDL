import afLib

class AFNState:
    state_counter = 0
    states = set()

    def __init__(self):
        self.name = str(AFNState.state_counter)
        AFNState.state_counter += 1
        AFNState.states.add(self)

        self.transitions = {}
        self.is_accept = False

class AFN:
    def __init__(self):
        self.start = None
        self.accept = None
        self.states = set()
        
def ast_to_afn(node,left_start=None,start_node=True):
    if not node:
        return None
    
    afn = AFN()
    
    # Un nodo básico con un carácter
    if node.value not in ['|', '.', '*']:
        if left_start:
            start = left_start
        else:
            start = AFNState()
            
        accept = AFNState()
        if start_node:
            accept.is_accept = True
            
        start.transitions[node.value] = [accept]
        afn.start = start
        afn.accept = accept
    elif node.value == '|':
        if left_start:
            start = left_start
        else:
            start = AFNState()
            
        afn_left = ast_to_afn(node=node.left,start_node=False)
        afn_right = ast_to_afn(node=node.right,start_node=False)
            
        accept = AFNState()
        if start_node:
            accept.is_accept = True
        
        start.transitions['ε'] = [afn_left.start, afn_right.start]
        afn_left.accept.transitions['ε'] = [accept]
        afn_right.accept.transitions['ε'] = [accept]
        
        afn.start = start
        afn.accept = accept
    elif node.value == '*':
        if left_start:
            start = left_start
        else:
            start = AFNState()
            
        afn_inner = ast_to_afn(node=node.right,start_node=False)
        
        accept = AFNState()
        if start_node:
            accept.is_accept = True
        
        start.transitions['ε'] = [afn_inner.start, accept]
        afn_inner.accept.transitions['ε'] = [afn_inner.start, accept]
        
        afn.start = start
        afn.accept = accept
    elif node.value == '.':
        if left_start:
            afn_left = ast_to_afn(node=node.left,left_start=left_start,start_node=False)
        else:
            afn_left = ast_to_afn(node=node.left,start_node=False)
        
        afn_right = ast_to_afn(node=node.right,left_start=afn_left.accept,start_node=False)
        
        afn.start = afn_left.start
        afn.accept = afn_right.accept
        if start_node:
            afn.accept.is_accept = True

    return afn

def AFN_simulation(afn,w):
    F = set()
    F.add(afn.accept)
    
    So = set()
    So.add(afn.start)
    
    S = afLib.e_closure(So)

    for c in w:
        S = afLib.e_closure(afLib.move(S,c))
        
    if F.intersection(S):
        return "sí"
    else:
        return "no"