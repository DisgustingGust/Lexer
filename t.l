%{		
	#include<stdio.h>
	#include<string.h>
	int _column = 1, _line = 1;
	int _FFlag = 0;
	char a[100000]="\0";
	void pr(const char *type, const char *txt, char a[]);
%}

%%
(\/\/[^\n]*(\n|$)) { /*однострочные*/
	if(_FFlag == 0){
		char comm[yyleng];
		strncpy(comm,yytext+2,yyleng-2);
		comm[yyleng-3] = '\0';
		pr("Comment",comm, a);
	}
	_line+=1;
	_column=1;
}


[(][*]((([^*])*([^)])*)|((([^*])*([^)])*[*][^)]+[)]([^*])*([^)])*))*)[*][)] {
	if(_FFlag == 1){
		for(int i = 0; i < yyleng; i++){
			_column += 1;
			if(yytext[i]=='\n'){
				_column = 1;
				_line += 1;
			}
		}
	}
	else{
		int _startL = _line;
		int _startC = _column;
		int _endC = _column;
		for(int i = 0; i < yyleng; i++) {
			_endC = _column;
			_column += 1;
			if(yytext[i] == '\n') {
				_column = 1;
				_line += 1;
			}
		}

		char comm[yyleng];
		strncpy(comm,yytext+2,yyleng-2);
		comm[yyleng-4] = '\0';
		char temp[100];
		sprintf(temp, "Comment(\"%s\", %d, %d, %d, %d); ", comm, _startL, _line, _startC, _endC);
		
		strcat(a, temp);
	}
}

"**" {
	pr("Op", yytext, a);
}

[\n] { /*отсеивание пробелов*/ 
	_line += 1;
	_column = 1;
}

[ \t] {
	_column += 1;
}


"skip" { /*ключевые слова*/
	pr("KW_SKIP", NULL, a);
}

"write" {
	pr("KW_WRITE", NULL, a);
}

"read" {
	pr("KW_READ", NULL, a);
}

"while" {
	pr("KW_WHILE", NULL, a);
}

"do" {
	pr("KW_DO", NULL, a);
}

"if" {
	pr("KW_IF", NULL, a);
}

"then" {
	pr("KW_THEN", NULL, a);
}

"else" {
	pr("KW_ELSE", NULL, a);
}


"\;" { /*присвоение и конец операции*/
	pr("Colon", NULL, a);
}

":=" {
	pr("Assignment", NULL, a);
}


[a-zA-Z_][a-zA-Z_0-9]* { /*переменные*/
	pr("Var", yytext, a);
}


([+|\-|/|%|>|<|*])|([=|\!]=)|([>|<]=)|(&&)|(\|\|) {
 /*операции*/
	pr("Op", yytext, a);
}


([1-9][0-9]*)|(0) { /*числа*/
	pr("Num", yytext, a);
}

(\(|\)) { /*скобки*/
	pr("Parenthesis", yytext, a);
}


[^ \r\n] { /*все остальное*/
	char temp[1000];
	sprintf(temp,"\nERROR! Line %d, columns %d-%d, content: %s\nLexer has been stopped!", _line, _column, _column+yyleng-1, yytext);
	strcat(a, temp);
	return 1;
}




%%

void pr(const char *type, const char *txt, char a[]) {
	char temp[1000];
	if(txt != NULL){
		sprintf(temp,"%s(\"%s\", %d, %d, %d); ",type, txt, _line, _column, _column+yyleng-1);
	}
	else{
		sprintf(temp,"%s(%d, %d, %d); ",type, _line, _column, _column+yyleng-1);
	}
	strcat(a, temp);
	_column += yyleng;
}

void main(int argc,char *argv[])
{
	if(!strcmp(argv[1], "-filter"))	{
		_FFlag=1;
		yyin=fopen(argv[2],"r");
	}
	else
		yyin=fopen(argv[1],"r");	
	
	if(yyin==NULL)
		printf("File does not exist\n");	
	else{
		yylex();
		printf("%s\n", a);
	}	
}

