import lexer as lexer
import ply.yacc as yacc
from datastructures import quadruples, types, operands, operators, variableTable
from datastructures import functionDir, temp, currentScope, currentType, semanticCube

tokens = lexer.tokens

def p_program(t):
    'program : PROGRAM ID programA1 SEMICOLON programVars programFunc main'
    print("Code valid")
    # show variable table and function directory
    # print()
    # for i in functionDir:
    #     print("\tfunction name: %s" % i)
    #     print("\t\ttype: %s" % functionDir[i]["type"])
    #     print("\t\tvars: %s" % functionDir[i]["vars"])
    #     print()
    
    operands.print()
    types.print()
    operators.print()
    quadruples.print()
    variableTable.clear()

# global scope varTable
def p_globalTable(t):
    'programA1 : '
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
    'main : mainA1 MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

# main scope varTable
def p_mainTable(t):
    'mainA1 : '
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
    if t[1] in variableTable[currentScope]:
        if types.pop() == variableTable[currentScope][t[1]]["type"]:
            quadruples.push(("=", operands.pop(), None, t[1]))
        else:
            print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
            exit(0)
    elif t[1] in variableTable["global"]:
        if types.pop() == variableTable["global"][t[1]]["type"]:
            quadruples.push(("=", operands.pop(), None, t[1]))
        else:
            print("Error: type mismatch in assignment for '%s' in line %d" % (t[1], t.lexer.lineno - 1))
            exit(0)

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
    'vars : ID varsA1 varsArray varsComa'

# add vars to varTable
def p_addToTable(t):
    'varsA1 : '
    # If current ID (t[-1]) exists in scope or global, throw error
    if t[-1] in variableTable[currentScope]:
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
    '''function : functionType ID functionA1 LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType ID functionA1 LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''
    # When exiting function scope, reset scope to global and delete variableTable and reference to it in functionDir
    global currentScope
    # del variableTable[currentScope]
    # del functionDir[currentScope]["vars"]
    currentScope = "global"

# add function to dir
def p_addToDir(t):
    'functionA1 : '
    # If function exists in global scope, throw an error
    if t[-1] in functionDir["global"] or t[-1] in variableTable["global"]:
        print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        global currentScope
        global currentType
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
                    | FUNCTION VOID functionTypeA1'''

# set void as current type
def p_setVoid(t):
    'functionTypeA1 : '
    # Set void as currentType
    global currentType
    currentType = t[-1]

def p_param(t):
    'param : primitive ID paramA1 functionParam'

# add function params to table
def p_addFuncParams(t):
    'paramA1 : '
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
    '''cst_prim : CST_INT cstprimA1
                | CST_FLOAT cstprimA2
                | CST_CHAR cstprimA3'''
    t[0] = t[1]

# add type int
def p_addTypeI(t):
    'cstprimA1 : '
    types.push("int")

# add type float
def p_addTypeF(t):
    'cstprimA2 : '
    types.push("float")

# add type char
def p_addTypeC(t):
    'cstprimA3 : '
    types.push("char")

def p_hyperExpression(t):
    '''hyperExpression : superExpression hyperExpA1 opHyperExpression hyperExpressionNested
                       | superExpression opMatrix 
                       | superExpression hyperExpA1'''

def p_hyperExpressionNested(t):
    '''hyperExpressionNested : superExpression hyperExpA1 opHyperExpression hyperExpressionNested
                             | superExpression hyperExpA1'''

def p_opConsumeHyperExp(t):
    'hyperExpA1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == "|" or operators.peek() == "&":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                quadruples.push((oper, lOp, rOp, "t%d"%temp))
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_opMatrix(t):
    '''opMatrix : EXCLAMATION addOperator
                | QUESTION addOperator
                | DOLLARSIGN addOperator '''

def p_opHyperExpression(t):
    '''opHyperExpression : AND addOperator
                         | OR addOperator '''

def p_superExpression(t):
    '''superExpression : exp superExpA1 opSuperExpression exp superExpA1
                       | exp superExpA1 '''

def p_opConsumeSuperExp(t):
    'superExpA1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek == "==":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                quadruples.push((oper, lOp, rOp, "t%d"%temp))
                quadruples.peek()
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_opSuperExpression(t):
    '''opSuperExpression : GT addOperator
                         | LT addOperator
                         | NOTEQUAL addOperator 
                         | ISEQUAL addOperator'''

def p_exp(t):
    '''exp : term termA1 expFunction
           | term termA1 '''

def p_opConsumeExp(t):
    'termA1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == "+" or operators.peek() == "-":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                quadruples.push((oper, lOp, rOp, "t%d"%temp))
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_expFunction(t):
    '''expFunction : PLUS addOperator exp
                   | MINUS addOperator exp '''

def p_term(t):
    '''term : factor factorA1 termFunction
            | factor factorA1 '''

def p_opConsumeTerm(t):
    'factorA1 : '
    global temp
    if operators.size() != 0:
        if operators.peek() == "*" or operators.peek() == "/":
            rOp = operands.pop()
            lOp = operands.pop()
            oper = operators.pop()
            rType = types.pop()
            lType = types.pop()
            resType = semanticCube[(lType, rType, oper)]
            if resType != "error":
                quadruples.push((oper, lOp, rOp, "t%d"%temp))
                operands.push("t%d"%temp)
                types.push(resType)
                temp += 1
            else:
                print("Error: type mismatch between '%s' and '%s' in line %d" % (lOp, rOp, t.lexer.lineno))
                exit(0)

def p_termFunction(t):
    '''termFunction : MULTIPLY addOperator term
                    | DIVIDE addOperator term '''

def p_addOperator(t):
    'addOperator : '
    operators.push(t[-1])

def p_factor(t):
    '''factor : LEFTPAR hyperExpression RIGHTPAR
              | cst_prim addOperand
              | module
              | ID addOperand addTypeId'''

def p_addOperand(t):
    'addOperand : '
    operands.push(t[-1])

def p_addTypeId(t):
    'addTypeId : '
    types.push(variableTable[currentScope][t[-2]]["type"])

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
                     | print_param '''

def p_printFunction2(t):
    'printFunction2 : printFunction'

def p_print_param(t):
    '''print_param : hyperExpression
                   | CST_STRING '''

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
    exit(0)

f = open('prog.txt', 'r')
program = f.read()

parser = yacc.yacc()

parser.parse(program)