# Patito++ PLY

import ply.lex as lex

reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void': 'VOID',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'read': 'READ',
    'print': 'PRINT',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'to': 'TO',
    'for': 'FOR'
}

tokens = [
    'GT',
    'LT',
    'AND',
    'OR',
    'NOTEQUAL',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'LEFTPAR',
    'RIGHTPAR',
    'EQUAL',
    'COMA',
    'SEMICOLON',
    'ID',
    'LEFTBRACK',
    'RIGHTBRACK',
    'LEFTBRACE',
    'RIGHTBRACE',
    'EXCLAMATION',
    'QUESTION',
    'DOLLARSIGN',
    'CST_INT',
    'CST_FLOAT',
    'CST_STRING',
    'CST_CHAR',
    'COMMENT_TEXT'
] + list(reserved.values())

# Tokens

t_GT            = r'>'
t_LT            = r'<'
t_AND           = r'&'
t_OR            = r'\|'
t_NOTEQUAL      = r'<>'
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_DIVIDE        = r'/'
t_MULTIPLY      = r'\*'
t_LEFTPAR       = r'\('
t_RIGHTPAR      = r'\)'
t_EQUAL         = r'='
t_COMA          = r','
t_SEMICOLON     = r';'
t_LEFTBRACK     = r'\['
t_RIGHTBRACK    = r'\]'
t_LEFTBRACE     = r'\{'
t_RIGHTBRACE    = r'\}'
t_EXCLAMATION   = r'!'
t_QUESTION      = r'\?'
t_DOLLARSIGN    = r'\$'
t_CST_INT       = r'[0-9]+'
t_CST_FLOAT     = r'[0-9]+\.[0-9]+'
t_CST_STRING    = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
t_CST_CHAR      = r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')'
t_COMMENT_TEXT  = r'%%.*\n'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Ignored characters
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s' in line %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
    exit(0)

lexer = lex.lex()

f = open('prog.txt', 'r')
program = f.read()

lex.lex()
# lex.input(program)
# while 1:
#     tok = lex.token()
#     if not tok: break
#     print(tok)

import ply.yacc as yacc

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
    'return : RETURN LEFTPAR hyperExpression RIGHTPAR'

def p_if(t):
    'if : IF LEFTPAR hyperExpression RIGHTPAR THEN LEFTBRACE statement RIGHTBRACE ifElse'

def p_ifElse(t):
    '''ifElse : ELSE LEFTBRACE statement RIGHTBRACE
              | '''

def p_comment(t):
    'comment : COMMENT_TEXT'

def p_while(t):
    'while : WHILE LEFTPAR hyperExpression RIGHTPAR DO statement'

def p_for(t):
    'for : FOR forDeclaration TO hyperExpression DO statement'

def p_forDeclaration(t):
    'forDeclaration : ID EQUAL CST_INT'

def p_vars(t):
    'vars : ID varsArray'

def p_varsComa(t):
    '''varsComa : COMA vars
                | '''

def p_varsArray(t):
    '''varsArray : LEFTBRACK CST_INT RIGHTBRACK varsMatrix varsComa
                 | varsComa '''

def p_varsMatrix(t):
    '''varsMatrix : LEFTBRACK CST_INT RIGHTBRACK varsComa
                  | varsComa '''

def p_function(t):
    '''function : functionType LEFTPAR param RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE
                | functionType LEFTPAR RIGHTPAR SEMICOLON LEFTBRACE statement RIGHTBRACE '''

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
                 | if statementFunction
                 | comment statementFunction
                 | read statementFunction
                 | print statementFunction
                 | assignment statementFunction
                 | declaration statementFunction
                 | module statementFunction
                 | for statementFunction
                 | while statementFunction
                 | '''

def p_statementFunction(t): 
    'statementFunction : statement'

def p_module(t):
    'module : ID LEFTPAR moduleFunction'

def p_moduleFunction(t):
    '''moduleFunction : ID COMA moduleFunction
                      | ID RIGHTPAR
                      | hyperExpression COMA moduleFunction
                      | hyperExpression RIGHTPAR'''

def p_error(t):
    print("Syntax error: Unexpected token '%s' in line %d" % (t.value, t.lexer.lineno))

parser = yacc.yacc()

parser.parse(program)