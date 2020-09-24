import re

def parseRPN(expression , strToFunDict , unOper , binOper):
    """
        Turns a RPN expression into a function.

        Arguments:
            expression - string with RPN expression
            strToFunDict - {<string with regular expression> : <function that turns the regular expression to a function> , ...}
            unOper - {<string with regular expression for unary operator> : <function function -> function>}
            binOper - {<string with regular expression for binary operator> : <function (function , function) -> function>}
    """
    wds = expression.split()
    fun_stack = [] 
    for w in wds:
        match = 0

        match_fun = []
        match_fun_s = []
        for reg in strToFunDict:
            match_fun_s.append(reg)
            if(re.match(reg , w)):
                match += 1
                match_fun.append(strToFunDict[reg])

        match_un = []
        match_un_s = []
        for reg in unOper:
            match_un_s.append(reg)
            if(re.match(reg , w)):
                match += 1
                match_un.append(unOper[reg])

        match_bin = []
        match_bin_s = []
        for reg in binOper:
            match_bin_s.append(reg)
            if(re.match(reg , w)):
                match += 1
                match_bin.append(binOper[reg])

        match_all_s = match_fun_s + match_un_s + match_bin_s

        if(match == 0):
            raise ValueError("Element of regular expression -" + w + "- matches none of strToFunDict, unOper, binOper: " + " ".join(match_all_s))
        elif(match > 1):
            raise ValueError("Element of regular expression -" + w + "- matches more then one of strToFunDict, unOper, binOper: " + " ".join(match_all_s))

        if(len(match_fun) == 1):
            fun_stack.append(match_fun[0](w))
        elif(len(match_un) == 1):
            if(len(fun_stack) > 0):
                part = fun_stack[:-1]
                rest = fun_stack[-1:]
                nf = match_un[0](rest[0])
                fun_stack = part + [nf]
            else:
                raise ValueError("Unary operator -" + match_un_s[0] + "- requires a stack of size at least 1.")
        elif(len(match_bin) == 1):
            if(len(fun_stack) > 1):
                part = fun_stack[:-2]
                rest = fun_stack[-2:]
                nf = match_bin[0](rest[0] , rest[1])
                fun_stack = part + [nf]
            else:
                raise ValueError("Binary operator -" + match_bin_s[0] + "- requires a stack of size at least 2.")
    if(len(fun_stack) != 1):
        raise ValueError("RPN expression schould leave stack with one element.")
    return fun_stack[0]

if(__name__ == "__main__"):
    funDict = {r"^[^+*-]*$" : lambda x : (lambda keys : x in keys)}
    unDict = {r"^[-]$" : lambda f : (lambda keys : not(f(keys)))}
    binDict = {r"^[*]$" : lambda f , g : (lambda keys : (f(keys) and g(keys))) , r"^[+]$" : lambda f , g : (lambda keys : (f(keys) or g(keys)))}
    funp = parseRPN("aaa bbb *" , funDict , unDict , binDict)
    print(funp(["adfsaa" , "bbb" , "aaa"]))
    funp = parseRPN("aaa bbb +" , funDict , unDict , binDict)
    print(funp(["adfsaa" , "bbasdasb" , "aaa"]))
    funp = parseRPN("aaa bbb - *" , funDict , unDict , binDict)
    print(funp(["adfsaa" , "bkldfb" , "aaa"]))
    funp = parseRPN("aaa bbb - *" , funDict , unDict , binDict)
    print(funp(["adfsaa" , "bbb" , "aaa"]))
