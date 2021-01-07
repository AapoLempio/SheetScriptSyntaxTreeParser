#!/usr/bin/env python3

### This file was made by Aapo Lempiö, 
### Student id: H292635
### For the course compcs400-principles-of-programming-languages_2020-2021

### In this file it is checked if the syntax of the sheetscript code right.
### It's been done using the BNF metasyntax notation
### The non-Terminals that we want to print out to check the correctness of 
### the syntax are added to the nonTerminals list and later printed out in 
### the main.py
### This file relies on the PLY lexing and parsing tools lex and yacc

import sys
import tokenizer
from decimal import *

tokens = tokenizer.tokens
nonTerminals = []

def p_program(p):
    '''program              : statement_list
                            | function_or_variable_definitions statement_list'''
    nonTerminals.append('program')

def p_function_call(p):
    '''function_call : FUNC_IDENT LSQUARE arguments RSQUARE
                     | FUNC_IDENT LSQUARE RSQUARE'''
    call = 'function_call( ' + str(p[1]) +' )'
    nonTerminals.append(call)

def p_function_or_variable_definitions(p):
    '''function_or_variable_definitions : function_or_variable_definition
                                        | function_or_variable_definitions function_or_variable_definition'''

def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definition
                                       | function_definition
                                       | subroutine_definition'''

def p_variable_definitions(p):
    '''variable_definitions : variable_definition
                            | variable_definitions variable_definition'''

def p_function_definition(p):
    '''function_definition  : FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS statement_list END'''
    definition = 'function_definition( ' + str(p[2]) +' )'
    nonTerminals.append(definition)

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''

def p_statement(p):
    '''statement : PRINT_SHEET INFO_STRING SHEET_IDENT
                 | PRINT_SHEET SHEET_IDENT
                 | PRINT_RANGE INFO_STRING range_expr
                 | PRINT_RANGE range_expr
                 | PRINT_SCALAR INFO_STRING scalar_expr
                 | PRINT_SCALAR scalar_expr
                 | IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                 | IF scalar_expr THEN statement_list ENDIF
                 | WHILE scalar_expr DO statement_list DONE
                 | FOR range_list DO statement_list DONE
                 | RETURN scalar_expr
                 | RETURN range_expr
                 | subroutine_call
                 | assignment'''
    if p[1] is not None:
        statement = 'statement( ' + str(p[1]) +' )'
        nonTerminals.append(statement)

def p_assignment(p):
    '''assignment : IDENT ASSIGN scalar_expr
                  | cell_ref ASSIGN scalar_expr
                  | RANGE_IDENT ASSIGN range_expr
                  | SHEET_IDENT ASSIGN SHEET_IDENT'''
    if p[1]:
        nonTerminals.append('assignment( ' + str(p[1]) + ' )')

def p_subroutine_definition(p):
    '''subroutine_definition : SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS variable_definitions statement_list END
                             | SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS variable_definitions statement_list END
                             | SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS statement_list END
                             | SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS statement_list END'''
    
    nonTerminals.append('subroutine_definition( ' + str(p[2]) + ' )')

def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE arguments RSQUARE
                      | FUNC_IDENT LSQUARE RSQUARE'''
    nonTerminals.append('subroutine_call( ' + str(p[1]) + ' )')

def p_formals(p):
    '''formals : formal_arg
               | formals COMMA formal_arg'''

def p_formal_arg(p):
    '''formal_arg : IDENT COLON SCALAR
                  | RANGE_IDENT COLON RANGE
                  | SHEET_IDENT COLON SHEET'''

def p_range_list(p):
    '''range_list : range_expr
                  | range_list COMMA range_expr'''

def p_arguments(p):
    '''arguments : arg_expr
                 | arguments COMMA arg_expr'''

def p_arg_expr(p):
    '''arg_expr : scalar_expr
                | range_expr
                | SHEET_IDENT'''

#def p_empty(p):
#    'empty :'
#    pass

def p_error(p):
    if p is None:
        print("End Of File Error: The file ended abruptly")
    else:
        print(str(p.lineno) + ":Syntax Error (token:'" + str(p.value) + "')")
    raise SystemExit

def p_cell_ref(p):
    '''cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR
                | DOLLAR COLON RANGE_IDENT'''

def p_variable_definition(p):
    '''variable_definition : scalar_definition
                           | range_definition
                           | sheet_definition'''
    definition = 'variable_definition( ' + str(p[1]) +' )'
    nonTerminals.append(definition)

def p_sheet_definition(p):
    '''sheet_definition : SHEET SHEET_IDENT
                        | SHEET SHEET_IDENT sheet_init'''
    p[0] = str(p[2])+ ':' + str(p[1])

def p_sheet_init(p):
    '''sheet_init : EQ sheet_init_list
                  | EQ INT_LITERAL MULT INT_LITERAL'''

def p_sheet_init_list(p):
    '''sheet_init_list : LCURLY sheet_rows RCURLY
            sheet_rows : sheet_row
                       | sheet_rows sheet_row'''

def p_sheet_row(p):
    '''sheet_row : simple_expr 
                 | sheet_row COMMA simple_expr'''

def p_range_definition(p):
    '''range_definition : RANGE RANGE_IDENT
                        | RANGE RANGE_IDENT EQ range_expr'''
    p[0] = str(p[2])+ ':' + str(p[1])

def p_range_expr(p):
    '''range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | LSQUARE function_call RSQUARE
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''

def p_scalar_definition(p):
    '''scalar_definition : SCALAR IDENT
                         | SCALAR IDENT EQ scalar_expr'''
    p[0] = str(p[2])+ ':' + str(p[1])

#simple_expr { (EQ|NOTEQ|LT|LTEQ|GT|GTEQ) simple_expr}
def p_scalar_expr(p):
    '''scalar_expr : simple_expr
                   | scalar_expr EQ simple_expr
                   | scalar_expr NOTEQ simple_expr
                   | scalar_expr LT simple_expr
                   | scalar_expr LTEQ simple_expr
                   | scalar_expr GT simple_expr
                   | scalar_expr GTEQ simple_expr'''
    nonTerminals.append('scalar_expr')

#simple_expr { (EQ|NOTEQ|LT|LTEQ|GT|GTEQ) simple_expr}
def p_simple_expr(p):
    '''simple_expr : simple_expr PLUS term
                   | simple_expr MINUS term
                   | term'''

#term { (PLUS | MINUS) term }
def p_term(p):
    '''term : term MULT factor
            | term DIV factor
            | factor'''
    
    nonTerminals.append('term')

#[MINUS] atom
def p_factor(p):
    '''factor : MINUS atom
              | atom'''
    nonTerminals.append('factor')


def p_atom(p):
    '''atom : IDENT 
            | DECIMAL_LITERAL 
            | cell_ref 
            | function_call
            | NUMBER_SIGN range_expr
            | LPAREN scalar_expr RPAREN'''
    if p[1] is None:
        nonTerminals.append('atom')
    else:
        if str(p[1]).islower():
            nonTerminals.append('atom( ' + str(p[1]) +' )')   
        else:
            try:
                nonTerminals.append('atom( ' + str(Decimal(p[1])) +' )')
            except:
                nonTerminals.append('atom')

    

