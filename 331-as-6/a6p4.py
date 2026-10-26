#!/usr/bin/env python3

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
Problem 4
"""

from sys import flags
from collections import Counter
from a6p1 import getOccurences, ngramsFreqs
from a6p2 import keyScore
from a6p3 import bestSuccessor


ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"   # This is the true English letter frequency


def breakSub(cipherFile: str, textFile: str) -> None:
    """
    Inputs:
        cipherFile:
            'text_finnegan_cipher.txt' for testing
            'text_cipher.txt' for submission
            Path to the ciphertext file.

        textFile:
            'wells.txt'
            Path to the English reference text file.

    Outputs:
        Save deciphered text to the address 'text_plain.txt'
    """
    n = 2  # Use bigrams as required by the assignment
    
    with open(cipherFile, mode = 'r', encoding = 'utf-8') as f:
        ciphertext = f.read()

    with open(textFile, mode = 'r', encoding = 'utf-8') as f:
        wellstext = f.read()

    frequencytext = freqDict(wellstext).keys()
    frequencycipher = freqDict(ciphertext).keys()

    frequencymap = dict(zip(frequencycipher, frequencytext))
    frequencymap.update({' ': ' '})

    prevfrequencymap = {}
    bigram_map = ngramsFreqs(wellstext, n)

    while  frequencymap != prevfrequencymap:
        prevfrequencymap = frequencymap.copy()
        frequencymap = bestSuccessor(frequencymap, ciphertext, bigram_map, n)

    frequencymap['S'] = 'P'
    frequencymap['V'] = 'W'
    
    plaintext = freqDecrypt(frequencymap, ciphertext)

    with open('text_plain.txt', mode = 'w', encoding = 'utf-8') as f:
        f.write(plaintext)

    return None



def freqDict(ciphertext: str) -> dict:
    """
    Analyze the frequency of the letters
    """
    mapping = {}
    cleantext = [char.upper() for char in ciphertext if char.isalpha()]
    letterfreq = Counter(cleantext)
    if not letterfreq:
        return {}

    letterfreq = dict(sorted(letterfreq.items(), key=lambda item: (-item[1], item[0])))

    for i , key in enumerate(letterfreq.keys()):
        mapping.update({key: ETAOIN[i]})

    return mapping

def freqDecrypt(mapping: dict, ciphertext: str) -> str:
    """
    Apply the mapping to ciphertext
    """
    mappedtext = [''] * len(ciphertext)

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            mappedchar = mapping[char.upper()]
            mappedtext[i] = mappedchar
        else:
            mappedtext[i] = char

    return ''.join(mappedtext)

'''
Use this section to import your code from A6P1, A6P2, A6P3
-- Make sure to import the entire module, sometimes using import from your own files can cause issues in the grading script

'''
        
def test():
    breakSub('text_cipher.txt', 'wells.txt')
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    
if __name__ == "__main__" and not flags.interactive:
    test()