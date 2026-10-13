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
CMPUT 331 Assignment 2 Student Solution
September 2026
Author: Chris Scheerschmidt
"""

from typing import List
from itertools import permutations
from legacy_code.a2p3mod import decipherMessage
import re

def crackSharedKey(keyperms: list[list[int]], dict, cipher:str) -> str: 
    keymatches = [0] * len(keyperms)
    plaintext = ""

    for j, perm in enumerate(keyperms): #iter through possible key permutations, save index of each permutation
        plaintext = decipherMessage(perm, cipher)
        cipherlist = list(re.sub(r'[^A-Z\s]', '', plaintext.upper()).split())
    
        for word in cipherlist:
            if word not in dict: 
                pass
            else:
                print(plaintext)
                keymatches[j] = keymatches[j] + 1 

        if keymatches == len(cipherlist):
            return plaintext

    return plaintext

#generate all permutations of keys given keylength
def getKeys(keylength:int) -> list[list[int]] :
    genlist = [0] * keylength
    for i in range(1, keylength + 1):
        genlist[i-1] = i

    return [list(p) for p in permutations(genlist)]


#save words in dictionary.txt to set
def form_dictionary(text_address='dictionary.txt') -> set[str]:
    dict = set()
    with open(text_address, 'r', encoding = 'utf-8') as f:
        dict = {line.rstrip('\n') for line in f}

    return dict

def test():
    pass
    


from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
