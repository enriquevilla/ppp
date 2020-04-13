# Patito++ PLY

import ply.lex as lex
reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'read': 'READ',
    'print': 'PRINT',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'from': 'FROM',
    'to': 'TO'
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
    'COLON',
    'SEMICOLON',
    'ID',
    'LEFTBRACE',
    'RIGHTBRACE',
    'PERCENT',
    'CST_INT',
    'CST_FLOAT',
    'CST_STRING',
    'CST_CHAR',
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
t_EQUAL        = r'='
t_COMA          = r','
t_COLON         = r':'
t_SEMICOLON     = r';'
t_LEFTBRACE     = r'\{'
t_RIGHTBRACE    = r'\}'
t_PERCENT       = r'%'
t_CST_INT       = r'[0-9]+'
t_CST_FLOAT     = r'[0-9]+\.[0-9]+'
t_CST_STRING    = r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
t_CST_CHAR      = r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')'


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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
