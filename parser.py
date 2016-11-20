#coding=utf8
import sys
import ply.lex as lex
import ply.yacc as yacc
from node import Node
_filter = True

keywords = {
    'while': 'WHILE',
    'do': 'DO',
    'read': 'READ',
    'write':'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'skip': 'SKIP'
}

tokens = [
    'COMMENT',
    'LINECOMMENT',
    'COLON',
    'VAR',
    'ASSIGNMENT',
    'OP',
    'NUMBER',
    'PARENTHESIS',
    'DIV',
    'MULT'
] + list(keywords.values())
t_NUMBER = r'([1-9][0-9]*)|(0)'
t_PARENTHESIS = r'(\(|\))'
t_COLON = r'\;'
t_ASSIGNMENT = r':='

def t_LINECOMMENT(t):
    r'(//[^\n]*(\n|$))'
    t.lexer.lineno += 1
    if _filter:
        pass
    else:
        return t

def t_COMMENT(t):
    r'[(][*]((([^*])*([^)])*)|((([^*])*([^)])*[*][^)]+[)]([^*])*([^)])*))*)[*][)]'
    for i in t.value:
        if i == '\n':
            t.lexer.lineno += 1
    if _filter:
        pass
    else:
        return t

def t_DIV(t):
    r'/'
    t.type = 'OP'
    return t

def t_OP(t):
    r'([>|<]=)|([+|\-|%|<|>])|([=|\!]=)|(&&)|(\|\|)|[\*][\*]'
    return t

def t_MULT(t):
    r'\*'
    t.type = 'OP'
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value,'VAR')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    print("Illegal character '%s'" % t.value[0]*20)
    t.lexer.skip(1)


#
#
#
#

def p_program_state(p):
    '''program : state '''
    p[0] = Node('P', [p[1]])

def p_state_UNCOMMENT(p):
    '''state : COMMENT state
            | LINECOMMENT state '''
    pass

def p_state_skip(p):
    '''state : SKIP'''
    p[0] = Node('S', ['skip'])

def p_state_assignment(p):
    '''state : VAR ASSIGNMENT exp'''
    p[0] = Node('S', [Node('VAR', [p[1]]), ':=', p[3]])

def p_state_colon(p):
    '''state : state COLON state'''
    p[0] = Node('S', [p[1], p[3]])

def p_state_write(p):
    '''state : WRITE exp'''
    p[0] = Node('S', ['write', p[2]])

def p_state_read(p):
    '''state : READ VAR'''
    p[0] = Node('S', ['read',Node('VAR', [p[2]])])
    #p[0] = Node('read', [p[2]])

def p_state_while(p):
    '''state : WHILE exp DO state'''
    p[0] = Node('S', ['while', p[2], 'do', p[4]])

def p_state_if(p):
    '''state : IF exp THEN state ELSE state'''
    p[0] = Node('S', ['if', p[2], 'then', p[4], 'else', p[6]])

def p_exp_var(p):
    '''exp : VAR'''
    p[0] = Node('E', [Node('VAR', [p[1]])])

def p_exp_number(p):
    '''exp : NUMBER'''
    p[0] = Node('N', [p[1]])

def p_expression_notparenthesis(p):
    '''exp : exp operation exp'''
    p[0] = Node('E', [p[1], p[2], p[3]])

def p_expression_parenthesis(p):
    '''exp : PARENTHESIS exp operation exp PARENTHESIS'''
    p[0] = Node('E', ['(', p[2], p[3], p[4],')'])
    #p[0] = Node(p[2])

def p_operation_OP(p):
    '''operation : OP
                | MULT
                | DIV'''
    p[0] = Node('⊕', p[1])

def p_error(p):
    print("unexpected token '%s'" % p.value[0])

def out_parse(data):
    parser = yacc.yacc(start='program')
    result = parser.parse(data)
    return result