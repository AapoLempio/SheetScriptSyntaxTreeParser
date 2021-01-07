#!/usr/bin/env python3

import argparse
import codecs
from tokenizer import tokenize

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print('422806 Aapo Lempiö')
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open(ns.file, 'r', encoding='utf-8') as INFILE:
            # blindly read all to memory (what if that is a 42Gb file?)
            data = INFILE.read()
        tokenize(data)