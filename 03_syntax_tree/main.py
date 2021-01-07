#!/usr/bin/env python3

### This file was made by Aapo Lempiö, 
### Student id: H292635
### For the course compcs400-principles-of-programming-languages_2020-2021


import argparse
import codecs
from tokenizer import tokenize, lexer
import syntaxer
import tree_print
from ply import yacc

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print('H292635 Aapo Lempiö')
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open(ns.file, 'r', encoding='utf-8') as INFILE:
            # blindly read all to memory (what if that is a 42Gb file?)
            data = INFILE.read()
        #tokenize(data)
        import syntaxer
        parser = yacc.yacc(module=syntaxer)
        result = parser.parse(data, lexer=lexer, debug=False, tracking=True)
        tree_print.treeprint(result, "unicode")
        

        #print("#####################")
        ##f = open("tests/animals_result.txt", "a")
        #for nonTerminal in syntaxer.nonTerminals:
        #    #f.write(nonTerminal + "\n")
        #    print(nonTerminal)
        #print( 'syntax OK' )
        #f.close()
        