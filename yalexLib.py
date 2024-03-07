# -*- coding: iso-8859-1 -*-
import regexLib
import astLib
import afdLib
import afnLib
import afLib

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
    close_curly_bracket = "\"}\""
    #Unicamente con espace entre ''
    quotes = "'\'''\"'"
    backslash = "\"\\\""
    kleene = "\"*\""
    blank_space = "\"\s\""
    
    ws = f"[{delim_regex}]+"
    allLetter = f"{letter}\"ÁÉÍÓÚ\"\"áéíóú\""
    _id = f"[{letter}]([{letter}]|[{digit}])*"
    
    comment_regex = f"\(\*[{allLetter}{digit}{delim_regex}{especial_chars}{brackets}]*\*\)"
    definition_regex = f"let{ws}{_id}{ws}={ws}[{letter}{digit}{especial_chars}{brackets}{quotes}{backslash}{blank_space}{parens}{kleene}]+"
    rule_regex = f"rule{ws}tokens{ws}={ws}[{allLetter}{digit}{delim_regex}{especial_chars}{parens}{kleene}{brackets}{curly_brackets}{quotes}]+[{close_curly_bracket}]"
    
    def __init__(self):
        regex = [YalexRecognizer.comment_regex,YalexRecognizer.definition_regex,YalexRecognizer.rule_regex,YalexRecognizer.ws]
        self.afds = []
        for item in regex:
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
            self.afds.append(afdmin)
            afdLib.AFDState.state_counter = 'A'
            afdLib.AFDState.states = set()

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