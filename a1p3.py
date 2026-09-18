#!/usr/bin/python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 Chris Scheerschmidt
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential 
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including 
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
#---------------------------------------------------------------

"""
CMPUT 331 Assignment 1 Student Solution
September 2026
Author: Chris Scheerschmidt
"""

import re
from sys import flags
from a1p1 import encrypt, decrypt

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def crack_caesar(ciphertext: str, val_words: set) -> str:
    plaintext = ""
    plainlist = []
    matchlist = []
    matches = 0
    bestmatch = ""

    for letter in LETTERS:
        plaintext = decrypt(ciphertext, letter) 
        plainlist = re.sub(r'[^A-Z\s]', '', plaintext).split()
        
        for word in plainlist:

            if word in val_words:
                matches += 1

            if matches == len(plainlist):
                return plaintext, letter

        matchlist.append(matches)

    bestmatch = LETTERS[(matchlist.index(max(matchlist)))]

    return decrypt(ciphertext , bestmatch), bestmatch



    


def form_dictionary(text_address='carroll-alice.txt') -> set:
    word_set = set()

    with open(text_address, 'r', encoding = 'utf-8') as f:
        word_set.update(re.sub(r'[^A-Z\s]', '', f.read().upper()).split())

    return word_set

def test():
    sample = "THIS IS PROBLEM 2 OF ASSIGNMENT 1."
    key = "X"
    cracked, key = crack_caesar(encrypt(sample, key), form_dictionary())
    print(cracked, key)
    
    #assert crack_caesar('TBIZLJB QL TLKABOIXKA', form_dictionary()) == ('WELCOME TO WONDERLAND', 'X')


if __name__ == "__main__" and not flags.interactive:
    test()