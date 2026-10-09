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
from legacy_code.a1p1mod import get_map
from legacy_code.a2p3mod import decipherMessage
from legacy_code.a2p4mod import getKeys
from legacy_code.a1p3mod import crack_caesar

AKEYS = [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25] #modular inverses for english alphabet
CHAR_TO_INDEX, INDEX_TO_CHAR = get_map() #dict that transforms letter to index of letter in alphabet and vice versa

def crackAffine(ciphertext: str, akey: int, bkey:int):
    plaintext = ""
    decryptint = 0
    for char in ciphertext:
        if char.isalpha():
            decryptint = (akey * (CHAR_TO_INDEX[char] - bkey) ) % 26
            plaintext += INDEX_TO_CHAR[decryptint]
        else:
            plaintext += char

    return plaintext
            

def hack(ciphertype: str, ciphertext: str):
    """
    Decrypt a given ciphertext with either of these algorithm: caesar, transposition, or affine.
        Input: a line from `ciphers.txt`.
        Output: the decrypted message (or plaintext).
    """

    match ciphertype:
        case 'A':
            for akey in AKEYS:
                for bkey in range(0, 26):
                    plaintext = crackAffine(ciphertext, akey, bkey)
                    if isEnglish(plaintext):
                        return plaintext

        case 'C':
            return crack_caesar(ciphertext, ENGLISH_WORDS)[0]

        case 'T':
            ciphertext = ciphertext.strip()
            for i in range(1, 10):
                perms = getKeys(i)
                for perm in perms:
                    plaintext = decipherMessage(perm ,ciphertext)
                    if isEnglish(plaintext):
                        plaintext += '\n'
                        return plaintext

    return ""
            

def processing():
    # Add the processing steps here like reading form ciphers.txt, calling the hack function, writing to decrypted.txt, etc.
    with open("ciphers.txt") as f:
        ciphers = f.readlines()

    with open("decrypted.txt", "w", encoding= "utf-8") as f:

        for cipher in ciphers:
            f.write(hack(cipher[0], cipher[3:]))
    
    return 0
            

def test():
    # Test cases for the hack function. You can add more tests as needed.
    processing()

if __name__ == '__main__':
    test()