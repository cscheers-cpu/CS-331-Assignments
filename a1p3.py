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
    firstwords = []
    bestmatch = ""
    firstalpha = ""

    for letter in LETTERS:
        plaintext = decrypt(ciphertext, letter) 
        plainlist = re.sub(r'[^A-Z\s]', '', plaintext).split()
        firstwords.append(plainlist[0])

        for word in plainlist:
            if word in val_words:
                matches += 1

        matchlist.append(matches)
        matches = 0

    #get decryption with most matches
    #test if more than one decryption with this many matches
    #select decryption with plaintext that comes first alphabetically
    maxval = max(matchlist)
    print(maxval)
    for i, val in enumerate(matchlist):
         if val == maxval:
              if not firstalpha or firstwords[i] < firstalpha:
                   bestmatch = LETTERS[i]
                   
    return decrypt(ciphertext , bestmatch), bestmatch

def form_dictionary(text_address='carroll-alice.txt') -> set:
    word_set = set()

    with open(text_address, 'r', encoding = 'utf-8') as f:
        word_set.update(re.sub(r'[^A-Z\s]', '', f.read().upper()).split())

    return word_set

def test():
        sample = "bar"
        key = "S"
        cracked, key = crack_caesar(encrypt(sample, key), form_dictionary())
        print(cracked, key)

if __name__ == "__main__" and not flags.interactive:
    test()