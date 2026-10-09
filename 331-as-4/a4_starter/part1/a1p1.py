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
# gkondrak <at> ualberta.ca
#
#---------------------------------------------------------------
"""
CMPUT 331 Assignment 1 Student Solution
September 2026
Author: Chris Scheerschmidt
"""
from sys import flags
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#generate dicts
def get_map(letters=LETTERS) -> tuple[dict[str, int], dict[int, str]]:
    char_to_index = {}
    index_to_char = {}

    for index, character in enumerate(letters):
        char_to_index[character] = index
        index_to_char[index] = character

    return char_to_index, index_to_char

def encrypt(message: str, key: str) -> str:
    message = message.upper()
    char_to_index, index_to_char = get_map()

    #shift magnitude based on letter key
    shift = char_to_index[key]
    encrypted = ""

    #encrypt each char from plaintext by shifting right by var shift, store encrypted message in string encrypted
    #if non-char, just add as it is
    for letter in message:
        if letter in char_to_index:
            encrypted = encrypted + index_to_char[(char_to_index[letter] + shift) % len(LETTERS)]
        else:
            encrypted = encrypted + letter

    return encrypted

def decrypt(message: str, key: str) -> str:
    message = message.upper()
    char_to_index, index_to_char = get_map()

    #shift magnitude based on letter key
    shift = char_to_index[key]
    decrypted = ""

    #decrypt each char from encrypted message by shifting left by var shift. store decrypted message in string decrypted
    #if non char, add as is
    for letter in message:
        if letter in char_to_index:
            decrypted =  decrypted + index_to_char[(char_to_index[letter] - shift) % len(LETTERS)]    
        else:
            decrypted = decrypted + letter

    return decrypted

def test():
    pass
    
if __name__ == "__main__" and not flags.interactive:
    test()