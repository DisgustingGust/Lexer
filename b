#!/bin/bash

sudo apt-get install gcc
sudo apt-get install byacc flex
sudo lex t.l
sudo gcc lex.yy.c -lfl -o lexer
