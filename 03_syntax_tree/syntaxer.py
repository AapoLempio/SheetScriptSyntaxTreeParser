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

class STNode:
    def __init__(self, nodetype):
            self.nodetype = nodetype

def p_program(p):
    '''program : statement_list
               | function_or_variable_definitions statement_list'''
    p[0] = STNode('program')
    if len(p)<3:
        p[0].children_stmt_list = p[1].children_
    else:
        p[0].children_funcs_vars = p[1].children_
        p[0].children_stmt_list = p[2].children_
    #nonTerminals.append('program')

def p_function_call(p):
    '''function_call : FUNC_IDENT LSQUARE arguments RSQUARE
                     | FUNC_IDENT LSQUARE RSQUARE'''
    p[0] = STNode('function_call')
    node = STNode('FUNC_IDENT')
    node.value = p[1]
    p[0].child_name = node
    if len(p) == 5:
        p[0].children_args = p[3].children_
        usage = STNode('usage')
        usage.value = 'scalar'
        p[0].child_usage = usage

def p_function_or_variable_definitions(p):
    '''function_or_variable_definitions : function_or_variable_definition
                                        | function_or_variable_definitions function_or_variable_definition'''
    p[0] = STNode('funcvardefs')
    if len(p) < 3:
        p[0].children_ = [p[1]]
    else:
        p[0].children_ = p[1].children_
        p[0].children_.append(p[2])

def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definition
                                       | function_definition
                                       | subroutine_definition'''
    p[0] = p[1]

def p_variable_definitions(p):
    '''variable_definitions : variable_definition
                            | variable_definitions variable_definition'''  
    p[0] = STNode('vardefs')
    if len(p) < 3:
        p[0].children_ = [p[1]]
    else:
        p[0].children_ = p[1].children_
        p[0].children_.append(p[2])

def p_function_definition(p):
    '''function_definition  : FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS variable_definitions statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN SCALAR IS statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN RANGE IS statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN SCALAR IS statement_list END
                            | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN RANGE IS statement_list END'''
    #definition = 'function_definition( ' + str(p[2]) +' )'
    #nonTerminals.append(definition)

    p[0] = STNode('function_def')
    node = STNode('FUNC_IDENT')
    node.value = p[2]
    p[0].child_name = node
    p[0].children_formals = p[4].children_

    rettype = STNode('rettype')
    if str(p[5]) == ']':
        rettype.value = p[7]
    else:
        rettype.value = p[6]
    p[0].child_rettype = rettype

    p[0].children_vars = []
   
    if len(p) == 12:
        p[0].children_vars = p[9]
        p[0].children_stmt_list = p[10].children_
    elif len(p) == 11:
        if str(p[4]) == ']':
            p[0].children_vars = p[8]
        if str(p[5]) == ']':
            p[0].children_vars = p[9]
        p[0].children_stmt_list = p[9].children_
    elif len(p) == 10:
        p[0].children_stmt_list = p[8].children_

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    p[0] = STNode("statement_list")
    if len(p) < 3:
        p[0].children_ = [p[1]]
    else:
        p[0].children_ = p[1].children_
        p[0].children_.append(p[2])
    
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
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if str(p[1]) == 'return':
            p[0] = STNode('return')
            p[0].child_expr = p[2]
            usage = STNode('usage')
            usage.value = 'scalar'
            #usage.value = 'range'
            p[0].child_usage = usage
        elif str(p[1]) == 'print_sheet':
            p[0] = STNode('PRINT_SHEET')
            p[0].value = p[2]
        elif str(p[1]) == 'print_range':
            p[0] = STNode('PRINT_RANGE')
            p[0].value = p[2]
        else:
            p[0] = STNode('PRINT_SCALAR')
            p[0].value = p[2]

    elif len(p) == 4:
        if str(p[1]) == 'print_sheet':
            p[0] = STNode('print_sheet')
            p[0].value = p[2]
        elif str(p[1]) == 'print_range':
            p[0] = STNode('print_range')
            p[0].value = p[2]
        elif str(p[1]) == 'print_scalar':
            p[0] = STNode('print_scalar')
            p[0].value = p[2]
        else:
            p[0] = STNode(str(p[1]))
        infostr = STNode("InfoString")
        infostr.nodetype = 'infostring'
        infostr.value = str(p[2])
        p[0].child_infostr = infostr
        p[0].child_expr = p[3]
    elif len(p) == 6:
        p[0] = STNode('')
        if str(p[1]) == 'for':
            p[0].nodetype = 'for_stmt'
            p[0].children_ranges = p[2].children_
            p[0].children_stmt_list = p[4].children_
        elif str(p[1]) == 'if':
            p[0].nodetype = 'if_stmt'
            p[0].children_ranges = p[4].children_
            p[0].child_scalar = p[2]
        elif str(p[1]) == 'while':
            p[0].nodetype = 'while_stmt'
            p[0].children_ranges = p[4].children_
    elif len(p) == 8:
        p[0] = STNode('')
        if str(p[1]) == 'if':
            p[0].nodetype = 'if_stmt'
            p[0].children_ranges = p[4].children_
        else:
            p[0] = p[1]


    #statement = 'statement( ' + str(p[1]) +' )'
    #nonTerminals.append(statement)

def p_assignment(p):
    '''assignment : IDENT ASSIGN scalar_expr
                  | cell_ref ASSIGN scalar_expr
                  | RANGE_IDENT ASSIGN range_expr
                  | SHEET_IDENT ASSIGN SHEET_IDENT'''
    if p[1]:
        nonTerminals.append('assignment( ' + str(p[1]) + ' )')
    p[0] = STNode('scalar_assign')
    node = STNode("IDENT")
    node.value = p[1]
    var = STNode('scalar_ref')
    var.child_name = node
    p[0].child_var = var
    p[0].child_expr = p[3]

def p_subroutine_definition(p):
    '''subroutine_definition : SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS variable_definitions statement_list END
                             | SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS variable_definitions statement_list END
                             | SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS statement_list END
                             | SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS statement_list END'''
    
    #nonTerminals.append('subroutine_definition( ' + str(p[2]) + ' )')
    p[0] = STNode('function_def')
    node = STNode('FUNC_IDENT')
    node.value = p[2]
    p[0].child_name = node
    p[0].children_formals = p[4].children_

    rettype = STNode('rettype')
    if str(p[5]) == ']':
        rettype.value = p[7]
    else:
        rettype.value = p[6]
    p[0].child_rettype = rettype

    p[0].children_vars = []
   
    if len(p) == 12:
        p[0].children_vars = p[9]
        p[0].children_stmt_list = p[10].children_
    elif len(p) == 11:
        if str(p[4]) == ']':
            p[0].children_vars = p[8]
        if str(p[5]) == ']':
            p[0].children_vars = p[9]
        p[0].children_stmt_list = p[9].children_
    elif len(p) == 10:
        p[0].children_stmt_list = p[8].children_

def p_subroutine_call(p):
    '''subroutine_call : FUNC_IDENT LSQUARE arguments RSQUARE
                      | FUNC_IDENT LSQUARE RSQUARE'''
    #nonTerminals.append('subroutine_call( ' + str(p[1]) + ' )')
    p[0] = STNode('subroutine_call')
    node = STNode('FUNC_IDENT')
    node.value = p[1]
    p[0].child_name = node
    if len(p) == 5:
        p[0].children_args = p[3].children_
        usage = STNode('usage')
        usage.value = 'scalar'
        p[0].child_usage = usage

def p_formals(p):
    '''formals : formal_arg
               | formals COMMA formal_arg'''
    p[0] = STNode('asd')
    if len(p) < 4:
        p[0].children_ = [p[1]]
    else:
        p[0].children_ = p[1].children_
        p[0].children_.append(p[3])
    
def p_formal_arg(p):
    '''formal_arg : IDENT COLON SCALAR
                  | RANGE_IDENT COLON RANGE
                  | SHEET_IDENT COLON SHEET'''
    p[0] = STNode('formal_arg')
    node = STNode('')
    if str(p[3]) == 'sheet':
        node.nodetype = 'SHEET_IDENT'
    elif str(p[3]) == 'range':
        node.nodetype = 'RANGE_IDENT'
    else:
        node.nodetype = 'IDENT'
    
    node.value = p[1]
    p[0].child_named = node

def p_range_list(p):
    '''range_list : range_expr
                  | range_list COMMA range_expr'''
    p[0] = STNode('range_list')
    if len(p) < 4:
        p[0].children_ = [p[1]]
    else:
        p[0].children_ = p[1].children_
        p[0].children_.append(p[3])

def p_arguments(p):
    '''arguments : arg_expr
                 | arguments COMMA arg_expr'''
    p[0] = STNode('arg')
    if len(p) < 4:
        p[0].children_ = [p[1]]
    else:
        p[0].children_ = p[1].children_
        p[0].children_.append(p[3])

def p_arg_expr(p):
    '''arg_expr : scalar_expr
                | range_expr
                | SHEET_IDENT'''
    if isinstance(p[1], STNode):
        p[0] = p[1]
    else:
        p[0] = STNode('SHEET_IDENT')
        p[0].value = p[1]

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
    p[0] = STNode('cell_ref')
    if str(p[1]) == 'SHEET' or str(p[1]) == 'S':
        node = STNode('SHEET_IDENT')
        node.value = p[1]
        p[0].child_name = node
        coord = STNode('coord')
        coord.value = (p[3], 'd')
        p[0].child_coord = coord
    else:
        p[0] = STNode('sda')

def p_variable_definition(p):
    '''variable_definition : scalar_definition
                           | range_definition
                           | sheet_definition'''
    p[0] = p[1]
    #definition = 'variable_definition( ' + str(p[1]) +' )'
    #nonTerminals.append(definition)

def p_sheet_definition(p):
    '''sheet_definition : SHEET SHEET_IDENT
                        | SHEET SHEET_IDENT sheet_init'''
    p[0] = STNode('scalar_definition')
    node = STNode("SHEET_IDENT")
    node.value = p[2]
    p[0].child_name = node
    if len(p) == 4:
        p[0].child_init = p[3]

def p_sheet_init(p):
    '''sheet_init : EQ sheet_init_list
                  | EQ INT_LITERAL MULT INT_LITERAL'''
    if len(p) == 3:
        p[0] = p[2]

def p_sheet_init_list(p):
    '''sheet_init_list : LCURLY sheet_rows RCURLY'''
    p[0] = STNode('sheet_init_list')
    p[0].children_rows = p[2].children_
    
def p_sheet_rows(p):
    '''sheet_rows : sheet_row
                  | sheet_rows sheet_row'''
    p[0] = STNode('sheet_rows')
    if len(p) < 3:
        p[0].children_ = [p[1]]
    else:
        p[0].children_ = p[1].children_
        p[0].children_.append(p[2])

def p_sheet_row(p):
    '''sheet_row : simple_expr 
                 | sheet_row COMMA simple_expr'''
    p[0] = STNode('col_init_list')
    if len(p) < 4:
        p[0].children_col = [p[1]]
    else:
        p[0].children_col = p[1].children_col
        p[0].children_col.append(p[3])

def p_range_definition(p):
    '''range_definition : RANGE RANGE_IDENT
                        | RANGE RANGE_IDENT EQ range_expr'''
    #p[0] = str(p[2])+ ':' + str(p[1])
    if len(p) == 3:
        p[0] = STNode('RANGE_INDENT')
        p[0].nodetype = 'range_definition'
        p[0].value = p[1]
    else:
        p[0] = STNode('range_definition')
        p[0].child_name = p[2] + str(p[2])
        p[0].child_init = p[4]

def p_range_expr(p):
    '''range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | LSQUARE function_call RSQUARE
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = STNode('function_call')
        p[0].child_function = p[2]
    elif len(p) ==  5:
        p[0] = STNode('range')
        p[0].child_name = p[2]
        p[0].child_2 = p[4]
    elif  len(p) == 7:
        p[0] = STNode('expr')
        p[0].child_range = p[1]

def p_scalar_definition(p):
    '''scalar_definition : SCALAR IDENT
                         | SCALAR IDENT EQ scalar_expr'''
    p[0] = STNode('scalar_definition')
    node = STNode("IDENT")
    node.value = p[2]
    p[0].child_name = node
    if len(p) == 5:
        p[0].child_init = p[4]
    else:
        p[0].child_init = None

def p_scalar_expr(p):
    '''scalar_expr : simple_expr
                   | scalar_expr EQ simple_expr
                   | scalar_expr NOTEQ simple_expr
                   | scalar_expr LT simple_expr
                   | scalar_expr LTEQ simple_expr
                   | scalar_expr GT simple_expr
                   | scalar_expr GTEQ simple_expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = STNode('oper ' + str(p[2]))
        p[0].child_left = p[1]
        p[0].child_right = p[3]

    #nonTerminals.append('scalar_expr')

def p_simple_expr(p):
    '''simple_expr : simple_expr PLUS term
                   | simple_expr MINUS term
                   | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = STNode('oper ' + str(p[2]))
        p[0].child_left = p[1]
        p[0].child_right = p[3]

def p_term(p):
    '''term : term MULT factor
            | term DIV factor
            | factor'''
    #nonTerminals.append('term')
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = STNode('oper ' + str(p[2]))
        p[0].child_left = p[1]
        p[0].child_right = p[3]

def p_factor(p):
    '''factor : MINUS atom
              | atom'''
    #nonTerminals.append('factor')
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_atom(p):
    '''atom : IDENT 
            | DECIMAL_LITERAL 
            | cell_ref 
            | function_call
            | NUMBER_SIGN range_expr
            | LPAREN scalar_expr RPAREN'''
    if len(p) >= 3:
        #nonTerminals.append('atom')
        p[0] = p[2]
    else:
        if str(p[1]).islower():
            #nonTerminals.append('atom( ' + str(p[1]) +' )')
            p[0] = STNode("scalar_ref")
            name = STNode('IDENT')
            name.value = p[1]
            p[0].child_name = name
        else:
            try:
                #nonTerminals.append('atom( ' + str(Decimal(p[1])) +' )')
                p[0] = STNode("decimal_number")
                p[0].value = str(Decimal(p[1]))
            except:
                #nonTerminals.append('atom')
                p[0] = p[1]
    

