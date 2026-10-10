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
#---------------------------------------------------------------

"""
Nomenclator cipher
Author: Chris Scheerschmidt
"""

from old_stuff.a1p1 import get_map
import random
import re

CHAR_TO_INDEX, INDEX_TO_CHAR = get_map()

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def translateMessage(key: str, message: str, codebook: dict, mode: str):
    """
    Encrypt or decrypt using a nomenclator.
    Takes a substitution cipher key, a message (plaintext or ciphertext),
    a codebook dictionary, and a mode string ('encrypt' or 'decrypt')
    specifying the action to be taken. Returns a string containing the
    ciphertext (if encrypting) or plaintext (if decrypting).
    """
    raise NotImplementedError()

def encryptWord(word: str, key: str):
    temp_word = ""
    temp_char = ""
    temp_index = 0

    for char in word:
        if char.isalpha():
            temp_char = char.upper()
            temp_index = CHAR_TO_INDEX[temp_char]

            if char.isupper():
                temp_word += key[temp_index]
            else:
                temp_word += key[temp_index].lower()
        else:
            temp_word += char

    return temp_word

def searchPlainString(word: str, codebook: dict):
    temp_word = ""

    for value in codebook:
        codeword = re.search(value, word)
        if codeword:
            temp_word = re.sub(codeword.group(), '', word)
            if any(char.isalpha() for char in temp_word):
                return None
            else:
                return codeword.group()

    return None

def searchCipherString(word: str, codebook: dict):

    for codename, code_list in codebook.items():
        for code_num in code_list:
            nomenclator = re.search(code_num, word)
            if nomenclator:
                return codename, nomenclator.group()

    return None


def decryptWord(word: str, key: str):
    temp_word = ""
    temp_char = ""
    temp_index = 0

    for char in word:
        if char.isalpha():
            temp_char = char.upper()
            temp_index = key.index(temp_char)

            if char.isupper():
                temp_word += INDEX_TO_CHAR[temp_index]
            else:
                temp_word += INDEX_TO_CHAR[temp_index].lower()
        else:
            temp_word += char

    return temp_word



def encryptMessage(key: str, message: str, codebook: dict):
    messagelist = message.split()
    cipherlist = [""] * len(messagelist)
    temp_word = ""
    codeword = ""

    for i, word in enumerate(messagelist):
        temp_word = word.lower()
        codeword = searchPlainString(temp_word, codebook)

        if codeword is not None:
            word = re.sub(codeword, random.choice(codebook[codeword]), word)

        cipherlist[i] = encryptWord(word, key)

    return " ".join(cipherlist)


def decryptMessage(key: str, message: str, codebook: dict):
    messagelist = message.split()
    plaintextlist = [""] * len(messagelist)
    codeword, code_num, word = ""


    for i, word in enumerate(messagelist):
        result = searchCipherString(word, codebook)

        if result is not None:
            codeword, code_num = result
            word = re.sub(code_num, codeword, word)

        plaintextlist[i] = decryptWord(word, key)

    return " ".join(messagelist)
        





def test():
    # Provided tests.
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    plaintext = "X-ray machines cannot be brought here, as -ray* are very dangerous. Hello;ray! ray;"
    codebook = {'ray':['1']}
    ciphertext = encryptMessage(key, plaintext, codebook)
    print(ciphertext)
    assert ciphertext =="G-clh nlwisxar wlxxpj fa fcptuij iaca, lr -1* lca qach olxuacptr. Iammp;clh! 1;"
    # End of provided tests.

if __name__ == '__main__':
    test()


""" if char.isalpha():
            temp_char = char.upper()
            char_index = CHAR_TO_INDEX[char]
            if char.isupper():
                ciphertext[i] = temp_char
            else:
                ciphertext[i] = temp_char.lower()"""