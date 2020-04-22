import lexer as lexer
import ply.yacc as yacc

tokens = lexer.tokens

def p_program(t):
    'program : PROGRAM ID SEMICOLON programVars programFunc main'
    print("Code valid")

def p_programVars(t):
    '''programVars : declaration
                   | '''
    
def p_programFunc(t):
    '''programFunc : function programFunc
                   | '''

def p_main(t):
    'main : MAIN LEFTPAR RIGHTPAR LEFTBRACE statement RIGHTBRACE'

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
    'vars : ID varsArray varsComa'

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
    '''function : functionType ID LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType ID LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''

def p_functionType(t):
    '''functionType : FUNCTION primitive
                    | FUNCTION VOID '''

def p_param(t):
    'param : primitive ID functionParam'

def p_functionParam(t):
    '''functionParam : COMA param
                     | '''

def p_cst_prim(t):
    '''cst_prim : CST_INT
                | CST_FLOAT
                | CST_CHAR '''

def p_hyperExpression(t):
    '''hyperExpression : superExpression opHyperExpression superExpression
                       | superExpression matrixOperator'''

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

def p_term(t):
    '''term : factor termFunction
            | factor '''

def p_termFunction(t):
    '''termFunction : MULTIPLY term
                    | DIVIDE term ''' 

def p_factor(t):
    '''factor : LEFTPAR hyperExpression RIGHTPAR
              | cst_prim
              | module
              | ID '''

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