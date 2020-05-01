import lexer as lexer
import ply.yacc as yacc
import datastructures as ds

tokens = lexer.tokens
tp = 1

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
    print(ds.operands)
    print(ds.types)
    print(ds.operators)
    print(ds.quadruples)
    ds.variableTable.clear()

# global scope varTable
def p_globalTable(t):
    'programA1 : '
    # Initialize variableTable for global and set program name and type
    ds.variableTable[ds.currentScope] = {}
    ds.variableTable[ds.currentScope][t[-1]] = {"type": "program"}
    # Initialize functionDir for global scope
    ds.functionDir[ds.currentScope] = {}
    # Set type and vars as reference to variableTable["global"]
    ds.functionDir[ds.currentScope]["type"] = "void"
    ds.functionDir[ds.currentScope]["vars"] = ds.variableTable[ds.currentScope]

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
    ds.variableTable[ds.currentScope]["main"] = {"type": "void"}
    ds.currentScope = "main"
    # Initialize variableTable and functionDir for main scope
    ds.variableTable[ds.currentScope] = {}
    ds.functionDir[ds.currentScope] = {}
    # Set function type and vars as reference to variableTable["main"]
    ds.functionDir[ds.currentScope]["type"] = "void"
    ds.functionDir[ds.currentScope]["vars"] = ds.variableTable[ds.currentScope]

def p_assignment(t):
    'assignment : ID EQUAL hyperExpression SEMICOLON'
    ds.quadruples.append(("=", ds.operands.pop(), None, t[1]))

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
    ds.currentType = t[1]

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
    if t[-1] in ds.variableTable[ds.currentScope] or t[-1] in ds.variableTable["global"]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Add current ID (t[-1]) to variableTable[scope]
        ds.variableTable[ds.currentScope][t[-1]] = {"type": ds.currentType}

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
    # del variableTable[currentScope]
    # del functionDir[currentScope]["vars"]
    ds.currentScope = "global"

# add function to dir
def p_addToDir(t):
    'functionA1 : '
    # If function exists in global scope, throw an error
    if t[-1] in ds.functionDir["global"] or t[-1] in ds.variableTable["global"]:
        print("Error: redefinition of '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Add function to variableTable of ds.currentScope
        ds.variableTable[ds.currentScope][t[-1]] = {"type": ds.currentType}
        # Change scope to new function id
        ds.currentScope = t[-1]
        # Initialize variableTable and functionDir for new function id
        ds.variableTable[ds.currentScope] = {}
        ds.functionDir[ds.currentScope] = {}
        # Set new function type and vars as reference to variableTable[ds.currentScope]
        ds.functionDir[ds.currentScope]["type"] = ds.currentType
        ds.functionDir[ds.currentScope]["vars"] = ds.variableTable[ds.currentScope]

def p_functionType(t):
    '''functionType : FUNCTION primitive
                    | FUNCTION VOID functionTypeA1'''

# set void as current type
def p_setVoid(t):
    'functionTypeA1 : '
    # Set void as currentType
    ds.currentType = t[-1]

def p_param(t):
    'param : primitive ID paramA1 functionParam'

# add function params to table
def p_addFuncParams(t):
    'paramA1 : '
    # If function param exists in scope or globally, throw error
    if t[-1] in ds.variableTable[ds.currentScope] or t[-1] in ds.variableTable["global"]:
        print("Error: redefinition of variable '%s' in line %d." % (t[-1], t.lexer.lineno))
        exit(0)
    else:
        # Add function param to variableTable of ds.currentScope
        ds.variableTable[ds.currentScope][t[-1]] = {"type": ds.currentType}

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
    ds.types.append("int")

# add type float
def p_addTypeF(t):
    'cstprimA2 : '
    ds.types.append("float")

# add type char
def p_addTypeC(t):
    'cstprimA3 : '
    ds.types.append("char")

def p_hyperExpression(t):
    '''hyperExpression : superExpression opHyperExpression hyperExpression
                       | superExpression opMatrix genQuadMatOp
                       | superExpression'''

def p_genQuadMatOp(t):
    'genQuadMatOp : '
    # quadruples.append((t[-2], None, t[-1]))

def p_opMatrix(t):
    '''opMatrix : EXCLAMATION
                | QUESTION
                | DOLLARSIGN'''

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
    ds.operators.append(t[1])
    global tp
    ds.quadruples.append((ds.operators.pop(), ds.operands.pop(), ds.operands.pop(), "t%d"%tp))
    ds.operands.append("t%d"%tp)
    tp += 1

def p_term(t):
    '''term : factor termFunction
            | factor '''

def p_termFunction(t):
    '''termFunction : MULTIPLY term
                    | DIVIDE term ''' 
    ds.operators.append(t[1])
    global tp
    ds.quadruples.append((ds.operators.pop(), ds.operands.pop(), ds.operands.pop(), "t%d"%tp))
    ds.operands.append("t%d"%tp)
    tp += 1

def p_factor(t):
    '''factor : LEFTPAR hyperExpression RIGHTPAR
              | cst_prim addOp
              | module
              | ID addOp addTypeId'''

def p_addOp(t):
    'addOp : '
    ds.operands.append(t[-1])

def p_addTypeId(t):
    'addTypeId : '
    ds.types.append(ds.variableTable[ds.currentScope][t[-2]]["type"])

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