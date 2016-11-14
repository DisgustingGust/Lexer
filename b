#!/bin/bash

sudo apt-get install gcc
sudo apt-get install byacc flex
sudo apt-get install python3
sudo lex t.l
sudo gcc lex.yy.c -lfl -o lexer
