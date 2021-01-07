#!/usr/bin/env python3

### This file was made by Aapo Lempiö, 
### Student id: H292635
### For the course compcs400-principles-of-programming-languages_2020-2021

### In this file I've determined all the tokens for the lexing of the sheetscript code
### This file relies on the PLY lexing and parsing tools lex and yacc

import sys
import ply.lex as lex
from ply import yacc
from decimal import *


reserved = {
    'sheet': 'SHEET',
    'scalar': 'SCALAR',
    'range': 'RANGE',
    'do': 'DO',
    'done': 'DONE',
    'is': 'IS',
    'while': 'WHILE',
    'for': 'FOR',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'endif': 'ENDIF',
    'function': 'FUNCTION',
    'subroutine': 'SUBROUTINE',
    'return': 'RETURN',
    'end': 'END',
    'print_sheet': 'PRINT_SHEET',
    'print_scalar': 'PRINT_SCALAR',
    'print_range': 'PRINT_RANGE'
}
# names of tokens
tokens = [
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'LCURLY',
    'RCURLY',

    'COMMA',
    'DOTDOT',
    'SQUOTE',
    'COLON',
    'DOLLAR',
    'NUMBER_SIGN',

    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',

    'INFO_STRING',
    'COORDINATE_IDENT',
    'DECIMAL_LITERAL',
    'INT_LITERAL',
    'IDENT',
    'RANGE_IDENT',
    'SHEET_IDENT',
    'FUNC_IDENT'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'{'
t_RCURLY = r'}'

t_COMMA = r','
t_DOTDOT = r'\.\.'
t_SQUOTE = r"\'"
t_COLON = r':'
t_DOLLAR = r'\$'
t_NUMBER_SIGN = r'[#]'

t_EQ = r'='
t_NOTEQ = r'!='
t_LT = r'<'
t_LTEQ = r'<='
t_GT = r'>'
t_GTEQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'


def t_newline(t):
    r'\n|\r'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r'\.\.\.[^\.\.\.]+\.\.\.'


def t_FUNC_IDENT(t):
    r'[A-Z](?:[a-z][a-z0-9_]*){1,}'
    return t


def t_INFO_STRING(t):
    r'![^!]+!'
    t.value = t.value.strip('!')
    return t


def t_COORDINATE_IDENT(t):
    r'[A-Z]{1,2}[0-9]{1,3}'
    t.type = reserved.get(t.value, 'COORDINATE_IDENT')
    return t


def t_DECIMAL_LITERAL(t):
    r'-\d+\.\d|\d+\.\d'
    t.value = Decimal(t.value)
    return t


def t_INT_LITERAL(t):
    r'-\d+|\d+'
    t.value = int(t.value)
    return t


def t_IDENT(t):
    r'[a-z]([a-z]|[A-Z]|[0-9]|_)+'
    #r'[a-z]([a-z]|[A-Z]|[0-9]|_)+'
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_RANGE_IDENT(t):
    r'_([a-z]|[A-Z]|[0-9]|_)+'
    return t


def t_SHEET_IDENT(t):
    r'[A-Z]+'
    return t

# Define a rule so we can track line numbers



# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s' at line '%d' " % (t.value[0], t.lexer.lineno))
    sys.exit(0)


# Build the lexer
lexer = lex.lex()


def tokenize(data):


    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
