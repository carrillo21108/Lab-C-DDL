from ctypes import FormatError
import string

def tokenizeRegex(regex):
    tokens = []
    i = 0
    while i < len(regex):
        char = regex[i]

        # Caracter de escape
        if char == '\\':
            if i + 1 < len(regex):
                tokens.append(regex[i:i+2])
                i += 2
            else:
                tokens.append(char)
                i += 1
                
        # Inicio de clase de caracteres
        elif char == '[':
            clase_char = char
            i += 1
            
            first_i=i
            first_char = char
            
            while i < len(regex) and regex[i] != ']':
                clase_char += regex[i]
                i += 1
            if i < len(regex):  # Asegurarse de incluir el ']' si no se ha llegado al final de la regex
                clase_char += regex[i]
                tokens.append(clase_char)
                i += 1
            else:
                tokens.append(first_char)
                i=first_i

        # Operadores
        elif char in {'*', '+', '?', '|'}:
            tokens.append(char)
            i += 1

        # Grupos
        elif char in {'(', ')'}:
            tokens.append(char)
            i += 1

        # Caracteres literales y otros
        else:
            tokens.append(char)
            i += 1

    return tokens

def regexAlphabet(postfix):
    alphabet = set()
    reserved = ['|','*','.','ε']
    
    i=0
    while i<len(postfix):
        char = postfix[i]
        if char[0] == '\\':
            alphabet.add(char[1])
        elif char not in reserved:
            alphabet.add(char)
            
        i+=1
            
    return alphabet

def validateRegexSyntax(regex):
    if not balancedRegex(regex):
        return (False,"expresion no balanceada.")
    
    if not validOperators(regex):
        return (False,"expresion con uso invalido de operadores.")
    
    if not validChars(regex):
        return (False,"expresion con uso invalido de caracteres.")
    
    return (True,"")

def balancedRegex(regex):
    stack = []
    simbolos = {'(': ')'}

    for caracter in regex:
        if caracter in simbolos.keys():
            stack.append(caracter)
        elif caracter in simbolos.values():
            if not stack or simbolos[stack.pop()] != caracter:
                return False
    
    if len(stack) == 0:
        return True
    else:
        return False
    
def validOperators(regex):
    allOperators = {'|','?','+','*'}
    if regex[0] in allOperators:
        return False
    
    if regex[-1]=='|':
        return False
    
    for i in range(0,len(regex)-1):
        if regex[i]=='|' and regex[i+1] in allOperators:
            return False
    
    return True

def validChars(regex):
    invalidChars = {'.'}
    
    for c in regex:
        if c in invalidChars:
            return False
        
    return True

def getPrecedence(c):
    if c=='(':
        return 1
    elif c=='|':
        return 2
    elif c=='.':
        return 3
    elif c=='*':
        return 4
    
def formatRegEx(tokens):
    allOperators = ['|', '?', '+', '*']
    binaryOperators = ['|']
    res = []
    
    # Función auxiliar para manejar los casos de '+' y '?'
    def handle_operator(index, operator, empty_symbol='ε'):
        nonlocal tokens
        if tokens[index - 1] != ')':
            if operator == '+':
                tokens[index - 1:index + 1] = ['(',tokens[index - 1], tokens[index - 1], '*',')']
            elif operator == '?':
                tokens[index - 1:index + 1] = ['(', tokens[index - 1], '|', empty_symbol, ')']
        else:
            j = index - 2
            count = 0
            while j >= 0 and (tokens[j] != '(' or count != 0):
                if tokens[j] == ')':
                    count += 1
                elif tokens[j] == '(':
                    count -= 1
                j -= 1
            if tokens[j] == '(' and count == 0:
                if operator == '+':
                    tokens[j:index + 1] = ['(']+tokens[j:index] + tokens[j:index] + ['*'] +['(']
                elif operator == '?':
                    tokens[j:index + 1] = ['('] + tokens[j:index] + ['|', empty_symbol, ')']
                    
    def expand_character_class(char_class):
        start, end = char_class[2], char_class[3]
        expanded = '|'.join(chr(c) for c in range(ord(start), ord(end) + 1))
        return ['('] + [char for char in expanded] + [')']

    # Manejar los casos de '+'
    i = 0
    while i < len(tokens):
        if tokens[i] == '+':
            handle_operator(i, '+')
            continue  # Evita incrementar i para revisar el nuevo token en la misma posición
        i += 1

    # Manejar los casos de '?'
    i = 0
    while i < len(tokens):
        if tokens[i] == '?':
            handle_operator(i, '?')
            continue
        i += 1
        
    # Agregar operadores de concatenación y manejar clases de caracteres
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Verifica si el token actual es una clase de caracteres
        if token.startswith('[') and token.endswith(']'):
            expanded_tokens = expand_character_class(token)
            res.extend(expanded_tokens)
            
        else:
            res.append(token)
            
        # Agregar operadores de concatenación según sea necesario
        if i + 1 < len(tokens):
            next_token = tokens[i + 1]
            if token not in binaryOperators + ['('] and next_token not in allOperators + [')', '.']:
                res.append('.')
        i += 1
        
    
    return res

def shunting_yard(regex):

    postfix = []
    operators = ['|','*','.']
    stack = []
    tokens = tokenizeRegex(regex)
    formattedRegEx = formatRegEx(tokens)
    
    i=0
    while i<len(formattedRegEx):
        c = formattedRegEx[i]
        
        if c=='(':
            stack.append(c)
        elif c==')':
            while stack[-1]!='(':
                postfix.append(stack.pop())
            
            stack.pop()
        elif c in operators:
            while len(stack)>0:
                peekedChar = stack[-1]
                peekedCharPrecedence = getPrecedence(peekedChar)
                currentCharPrecedence = getPrecedence(c)
                
                if peekedCharPrecedence>=currentCharPrecedence:
                    postfix.append(stack.pop())
                else:
                    break
            
            stack.append(c)
        else:
            postfix.append(c)
        
        i+=1
    
    while len(stack)>0:
        postfix+=stack.pop()
    
    return postfix