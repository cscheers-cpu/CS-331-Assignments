#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 10/8/2026 Chris Scheerschmidt
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
#----------------------------------------------------------------

#-------------------- START ASSIGNMENT HERE ---------------------
"""
General decryption program
Author: Chris Scheerschmidt
"""

from detectEnglish import isEnglish, ENGLISH_WORDS
from itertools import permutations
from a2p3mod import decipherMessage
from a2p4mod import getKeys
import re
from a1p3mod import crack_caesar

def hack(ciphertype: str, ciphertext: str):
    """
    Decrypt a given ciphertext with either of these algorithm: caesar, transposition, or affine.
        Input: a line from `ciphers.txt`.
        Output: the decrypted message (or plaintext).
    """
    if ciphertype == "A":
        return ("")
    elif ciphertype == "C":
        return crack_caesar(ciphertext, ENGLISH_WORDS)[0]
    else:
        ciphertext = ciphertext.strip()
        for i in range(1, 10):
            perms = getKeys(i)
            for perm in perms:
                plaintext = decipherMessage(perm ,ciphertext)
                if isEnglish(plaintext):
                    return decipherMessage(perm, ciphertext)
            

def processing():
    # Add the processing steps here like reading form ciphers.txt, calling the hack function, writing to decrypted.txt, etc.
    with open("ciphers.txt") as f:
        ciphers = f.readlines()
        
    for cipher in ciphers:
        print(hack(cipher[0], cipher[3:]))
    
    return 0
            

def test():
    processing()
    # Test cases for the hack function. You can add more tests as needed.
    assert hack("C", "GHGIQ") == "ABACK", "Caesar hack failed"
    assert hack("T", "IS HAUCREERNP F") == "CIPHERS ARE FUN", "Transposition hack failed"
    assert hack("A", "IHHWVC SWFRCP") == "AFFINE CIPHER", "Affine hack failed"
    assert hack("A", "XBQUVSQVFRUVLE FVSOTG") == "MULTIPLICATION CIPHER", "Affine hack failed"

if __name__ == '__main__':
    test()