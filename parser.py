import lexer as lexer
import ply.yacc as yacc

import queue

tokens = lexer.tokens

functionDir = {}
variableTable = {}
semanticCube = {}
quadruples = []
operators = []
operands = []
types = []
temp = 1
ty = {
    0: "int",
    1: "float",
    2: "char"
}
ops = ["+", "-", "*", "/"]

# print("Semantic Cube: ")
for i in ty:
    for j in ty:
        for k in ops:
            if i > j:
                semanticCube[(ty[i], ty[j], k)] = ty[i]
            else:
                semanticCube[(ty[i], ty[j], k)] = ty[j]
            if k != "+" and (ty[i] == "char" or ty[j] == "char"):
                semanticCube[(ty[i], ty[j], k)] = "error"
            # print("%s %s %s = %s" % (types[i], k, types[j], semanticCube[(types[i], types[j], k)]))

currentScope = "global"
currentType = "program"
# functionDir visual example
'''
    "global": {
        "type": "void",
        "vars": variableTable["global"] -> "i": {
                                                "type": "int"
                                                "value": 1
                                            }
                                            ...
    }
    "main": {
        "type": "void",
        "vars": variableTable["main"] -> "c": {
                                              "type": "char"
                                              "value": "h"
                                         }
                                         ...
    }
'''

# semanticCube explanation
'''
    keys are tuples => (operand1, operand2, operator)

    semanticCube[(op1, op2, op)] => int/float/char/error

    semanticCube[("int", "int", "+")] => "int"
    semanticCube[("char", "float", "*")] => "error"
'''

def p_program(t):
    'program : PROGRAM ID globalTable SEMICOLON programVars programFunc main'
    print("Code valid")
    # show variable table and function directory
    # print()
    # for i in functionDir:
    #     print("\tfunction name: %s" % i)
    #     print("\t\ttype: %s" % functionDir[i]["type"])
    #     print("\t\tvars: %s" % functionDir[i]["vars"])
    #     print()
    print(operands)
    print(types)
    print(operators)
    variableTable.clear()

def p_globalTable(t):
    'globalTable : '
    # Initialize variableTable for global and set program name and type
    variableTable[currentScope] = {}
    variableTable[currentScope][t[-1]] = {"type": "program"}
    # Initialize functionDir for global scope
    functionDir[currentScope] = {}
    # Set type and vars as reference to variableTable["global"]
    functionDir[currentScope]["type"] = "void"
    functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_programVars(t):
    '''programVars : declaration
                   | '''

def p_programFunc(t):
    '''programFunc : function programFunc
                   | '''

def p_main(t):
    'main : mainScope MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_mainScope(t):
    'mainScope : '
    global currentScope
    variableTable[currentScope]["main"] = {"type": "void"}
    currentScope = "main"
    # Initialize variableTable and functionDir for main scope
    variableTable[currentScope] = {}
    functionDir[currentScope] = {}
    # Set function type and vars as reference to variableTable["main"]
    functionDir[currentScope]["type"] = "void"
    functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_assignment(t):
    'assignment : ID EQUAL hyperExpression SEMICOLON'

def p_declaration(t):
    'declaration : VAR declarationPrim'

def p_declarationPrim(t):
    '''declarationPrim : primitive vars SEMICOLON declarationPrim
                       | '''

def p_primitive(t):
    '''primitive : INT
                 | FLOAT
                 | CHAR '''
    # When stating type, change currentType for declaration
    global currentType
    currentType = t[1]

def p_return(t):
    'return : RETURN LEFTPAR hyperExpression RIGHTPAR SEMICOLON'

def p_if(t):
    'if : IF LEFTPAR hyperExpression RIGHTPAR THEN LEFTBRACE statement RIGHTBRACE ifElse'

def p_ifElse(t):
    '''ifElse : ELSE LEFTBRACE statement RIGHTBRACE
              | '''

def p_comment(t):
    'comment : COMMENT_TEXT'

def p_while(t):
    'while : WHILE LEFTPAR hyperExpression RIGHTPAR LEFTBRACE statement RIGHTBRACE'

def p_for(t):
    'for : FOR forDeclaration TO hyperExpression LEFTBRACE statement RIGHTBRACE'

def p_forDeclaration(t):
    'forDeclaration : ID EQUAL CST_INT'

def p_vars(t):
    'vars : ID addToTable varsArray varsComa'
    
def p_addToTable(t):
    'addToTable : '
    # If current ID (t[-1]) exists in scope or global, throw error
    if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Add current ID (t[-1]) to variableTable[scope]
        variableTable[currentScope][t[-1]] = {"type": currentType}

def p_varsComa(t):
    '''varsComa : COMA vars
                | '''

def p_varsArray(t):
    '''varsArray : LEFTBRACK CST_INT RIGHTBRACK varsMatrix
                 | '''

def p_varsMatrix(t):
    '''varsMatrix : LEFTBRACK CST_INT RIGHTBRACK
                  | '''

def p_function(t):
    '''function : functionType ID addToDir LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType ID addToDir LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''
    # When exiting function scope, reset scope to global and delete variableTable and reference to it in functionDir
    global currentScope
    # del variableTable[currentScope]
    # del functionDir[currentScope]["vars"]
    currentScope = "global"
    
def p_addToDir(t):
    'addToDir : '
    global currentScope
    # If function exists in global scope, throw an error
    if t[-1] in functionDir["global"] or t[-1] in variableTable["global"]:
        print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Add function to variableTable of currentScope
        variableTable[currentScope][t[-1]] = {"type": currentType}
        # Change scope to new function id
        currentScope = t[-1]
        # Initialize variableTable and functionDir for new function id
        variableTable[currentScope] = {}
        functionDir[currentScope] = {}
        # Set new function type and vars as reference to variableTable[currentScope]
        functionDir[currentScope]["type"] = currentType
        functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_functionType(t):
    '''functionType : FUNCTION primitive
                    | FUNCTION VOID setVoid'''

def p_setVoid(t):
    'setVoid : '
    # Set void as currentType
    global currentType
    currentType = t[-1]

def p_param(t):
    'param : primitive ID addFuncParams functionParam'

def p_addFuncParams(t):
    'addFuncParams : '
    # If function param exists in scope or globally, throw error
    if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Add function param to variableTable of currentScope
        variableTable[currentScope][t[-1]] = {"type": currentType}

def p_functionParam(t):
    '''functionParam : COMA param
                     | '''

def p_cst_prim(t):
    '''cst_prim : CST_INT addTypeI
                | CST_FLOAT addTypeF
                | CST_CHAR addTypeC'''
    t[0] = t[1]

def p_addTypeI(t):
    'addTypeI : '
    types.append("int")

def p_addTypeF(t):
    'addTypeF : '
    types.append("float")

def p_addTypeC(t):
    'addTypeC : '
    types.append("char")

def p_hyperExpression(t):
    '''hyperExpression : superExpression opHyperExpression superExpression genQuad
                       | superExpression matrixOperator genQuadMatOp'''

def p_genQuad(t):
    'genQuad : '
    # quadruples.append((t[-3], t[-1], t[-2]))

def p_genQuadMatOp(t):
    'genQuadMatOp : '
    # quadruples.append((t[-2], None, t[-1]))

def p_matrixOperator(t):
    '''matrixOperator : EXCLAMATION
                      | QUESTION
                      | DOLLARSIGN
                      | '''

def p_opHyperExpression(t):
    '''opHyperExpression : AND
                         | OR '''

def p_superExpression(t):
    '''superExpression : exp opSuperExpression exp
                       | exp '''

def p_opSuperExpression(t):
    '''opSuperExpression : GT
                         | LT
                         | NOTEQUAL '''

def p_exp(t):
    '''exp : term expFunction
           | term '''

def p_expFunction(t):
    '''expFunction : PLUS exp
                   | MINUS exp ''' 
    operators.append(t[1])

def p_term(t):
    '''term : factor termFunction
            | factor '''

def p_termFunction(t):
    '''termFunction : MULTIPLY term
                    | DIVIDE term ''' 
    operators.append(t[1])

def p_factor(t):
    '''factor : LEFTPAR hyperExpression RIGHTPAR
              | cst_prim addOp
              | module
              | ID addOp addTypeId'''

def p_addOp(t):
    'addOp : '
    operands.append(t[-1])

def p_addTypeId(t):
    'addTypeId : '
    types.append(variableTable[currentScope][t[-2]]["type"])

def p_read(t):
    'read : READ LEFTPAR id_list RIGHTPAR SEMICOLON'

def p_id_list(t):
    'id_list : ID id_listFunction'

def p_id_listFunction(t):
    '''id_listFunction : COMA id_list
                       | '''

def p_print(t):
    'print : PRINT LEFTPAR printFunction RIGHTPAR SEMICOLON'

def p_printFunction(t):
    '''printFunction : print_param COMA printFunction2
                     | print_param'''

def p_printFunction2(t):
    'printFunction2 : printFunction'

def p_print_param(t):
    '''print_param : hyperExpression
                   | CST_STRING'''

def p_statement(t):
    '''statement : return
                 | if statement
                 | comment statement
                 | read statement
                 | print statement
                 | assignment statement
                 | declaration statement
                 | module statement
                 | for statement
                 | while statement 
                 | '''

def p_module(t):
    'module : ID LEFTPAR moduleFunction RIGHTPAR SEMICOLON'

def p_moduleFunction(t):
    '''moduleFunction : hyperExpression COMA moduleFunction
                      | hyperExpression RIGHTPAR
                      | '''

def p_error(t):
    print("Syntax error: Unexpected token '%s' in line %d" % (t.value, t.lexer.lineno))

f = open('prog.txt', 'r')
program = f.read()

parser = yacc.yacc()

parser.parse(program)