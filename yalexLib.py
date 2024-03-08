# -*- coding: iso-8859-1 -*-
import afdLib

class YalexRecognizer:
    #Son tomadas como espacio, tabulacion y salto de linea literal
    delim_regex = "\"\s\t\n\""
    letter = "'A'-'Z''a'-'z'"
    digit = "'0'-'9'"
    #Mejorable al considerar todos los caracteres ASCII
    especial_chars = "\",_+-.?|/:;=<>\""
    parens = "\"()\""
    brackets = "\"\[\]\""
    curly_brackets = "\"{}\""
    open_curly_bracket = "\"{\""
    close_curly_bracket = "\"}\""
    #Unicamente con espace entre ''
    quotes = "'\'''\"'"
    backslash = "\"\\\""
    kleene = "\"*\""
    blank_space = "\"\s\""
    
    ws = f"[{delim_regex}]+"
    allLetter = f"{letter}\"ÁÉÍÓÚ\"\"áéíóú\""
    _id = f"[{letter}]([{letter}]|[{digit}])*"
    
    let = "let"
    rule = "rule"
    tokens = "tokens"
    equal = "="
    
    string = f"[{quotes}][{letter}{digit}{especial_chars}{brackets}{quotes}{curly_brackets}{blank_space}{parens}{kleene}]+[{quotes}]"
    char = f"[{quotes}][{letter}{digit}]+[{quotes}]"
    
    union = "[\"|\"]"
    rule_return = f"[{open_curly_bracket}]{ws}return{ws}[{letter}]+{ws}[{close_curly_bracket}]"

    
    comment_regex = f"\(\*[{allLetter}{digit}{delim_regex}{especial_chars}{brackets}]*\*\)"
    definition_regex = f"{let}{ws}{_id}{ws}{equal}{ws}[{letter}{digit}{especial_chars}{brackets}{quotes}{backslash}{blank_space}{parens}{kleene}]+"
    rule_regex = f"{rule}{ws}{tokens}{ws}{equal}{ws}[{allLetter}{digit}{delim_regex}{especial_chars}{parens}{kleene}{brackets}{curly_brackets}{quotes}]+[{close_curly_bracket}]"
    
    def __init__(self):
        regex = [YalexRecognizer.comment_regex,YalexRecognizer.definition_regex,YalexRecognizer.rule_regex,YalexRecognizer.ws,YalexRecognizer.let,YalexRecognizer._id,YalexRecognizer.equal,YalexRecognizer.rule,YalexRecognizer.tokens,YalexRecognizer.string,YalexRecognizer.union,YalexRecognizer.rule_return,YalexRecognizer.char]
        self.afds = []
        for item in regex:
            self.afds.append(afdLib.createAFD(item))

    def step_simulate_AFD(self,afd_pos,c,lookAhead):
        afd = self.afds[afd_pos]
        res = afd.step_simulation(c, lookAhead)
        state = list(res)[0] if len(list(res))>0 else None

        if state in afd.accept:
            return 0
        elif state in afd.states:
            return 1
        else:
            return 2

    def step(self):
        pass