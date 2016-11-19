#coding=utf8

from parser import *
import ply.lex as lex

with open(sys.argv[-1], 'r') as my_file:
    data = my_file.read()
    lexer = lex.lex()
    print(out_parse(data))