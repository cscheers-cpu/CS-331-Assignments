#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 10/17/26 Chris Scheerschmidt
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
CMPUT 331 Assignment 5 Problem 3 Student Solution
Author: Chris Scheerschmidt
"""
#mapping that was found manually
MYMAP = {
        'A': 'A',
        'C': 'N',
        'D': 'O',
        'E': 'Y',
        'F': 'D',
        'G': 'G',
        'H': 'F',
        'I': 'B',
        'J': 'L',
        'K': 'R',
        'L': 'I',
        'M': 'S',
        'N': 'C',
        'Q': 'K',
        'S': 'U',
        'T': 'P',
        'U': 'V',
        'V': 'H',
        'W': 'M',
        'X': 'W',
        'Y': 'T',
        'Z': 'E',
    }

import a5p1
from sys import flags

def checkLetterFrequency(ciphertext: str) -> dict:
    if len(ciphertext) == 0:
        return {}
    
    cipherlen = 0
    letterdict = {}
    ciphertext = ciphertext.upper()

    for char in ciphertext:
        if char.isalpha():
            cipherlen += 1
            if char not in letterdict:
                letterdict.update({char: 1})
            else:
                letterdict[char] += 1

    for key in letterdict.keys():
        letterdict[key] = letterdict[key] / cipherlen

    return letterdict


#solve cipher with mapping that was found manually, save to plaintext.txt
def solveCipher(filename = 'ciphertext.txt'):
    with open(filename, 'r', encoding='utf-8') as f:
        ciphertext = f.read()

    ciphertext = a5p1.freqDecrypt(MYMAP, ciphertext)

    with open ('plaintext.txt', 'w', encoding='utf-8') as f:
        f.write(ciphertext)

    return 0

def test():
    pass

if __name__ == '__main__' and not flags.interactive:
    test()
