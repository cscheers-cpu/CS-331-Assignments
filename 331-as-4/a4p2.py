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

from legacy_code.a1p1mod import get_map
import random
import re

CHAR_TO_INDEX, INDEX_TO_CHAR = get_map()

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#encrypt plaintext
def encryptMessage(key: str, message: str, codebook: dict):
    codebook = {codeword.upper(): codenumbers for codeword, codenumbers in codebook.items()}
    messagelist = formatMessage(message)
    cipherlist = applyTransformation(messagelist, codebook, key, 'encrypt')

    ciphertext = ''.join(cipherlist)
    ciphertext = ciphertext.encode('utf-8').decode('unicode_escape')

    return ciphertext

#decrypt ciphertext
def decryptMessage(key: str, message: str, codebook: dict):
    messagelist = formatMessage(message)
    plainlist = applyTransformation(messagelist, codebook, key, 'decrypt')

    plaintext = ''. join(plainlist)
    plaintext = plaintext.encode('utf-8').decode('unicode_escape')
    
    return plaintext

#format message and preserve spaces (spaces are elements in list, not removed)
#escape sequences are characterified
def formatMessage(message):
    message = message.encode('unicode-escape').decode('utf-8')
    messagelist = []
    current_word = []

    for char in message:
        if char == ' ':
            if current_word:
                messagelist.append("".join(current_word))
                current_word = []
            messagelist.append(' ')
        else:
            current_word.append(char)

    if current_word:
        messagelist.append("".join(current_word))

    return messagelist

#iter through words in cipher/plaintext
#if escape char present, handle seperately
#else see if word is nomenclator/nomenclator code or regular text. handle accordingly
def applyTransformation(messagelist, codebook, key, mode):
    newlist = [""] * len(messagelist)

    for i, word in enumerate(messagelist):
        if re.search(r'\\[ntrvfb0]', word):
            esclist = re.split(r'(\\[ntr0vfb])', word)
            word = transformEscapeChar(esclist, r'\\[ntrvfb0]', codebook, key, mode)
           
        else:
            if mode == 'encrypt':
                word = testEncryptWord(word, codebook, key)
            else:
                word = testDecryptWord(word, codebook, key)

        newlist[i] = word

    return newlist

#split escape char from word, encrypt/decrypt remaining word[s]
#join back to one string after transformation
def transformEscapeChar(esclist, escsequences, codebook, key, mode):
    newlist = [""] * len(esclist)

    for i, word in enumerate(esclist):
        if re.search(escsequences, word):
            newlist[i] = word
        else:
            if mode == 'decrypt':
                word = testDecryptWord(word, codebook, key)
                newlist[i] = word

            if mode == 'encrypt':
                word = testEncryptWord(word, codebook, key)
                newlist[i] = word

    return ''.join(newlist)

#see if plainword is nomenclator or regular word
#encrypt accordingly
def testEncryptWord(word, codebook, key):
    codenumbers = searchPlainString(word.upper(), codebook)

    if codenumbers is not None:
        number = random.choice(codenumbers)
        if not word.isalnum():
            word = re.sub(r'[a-zA-Z0-9]+', number, word) #maintain punctuation and insert nomenclator
        else:
            word = number

    return encryptWord(word, key)


#see if cipherword is nomenclator
#decrypt accordingly
def testDecryptWord(word, codebook, key):
    word = decryptWord(word, key)
    codeword = searchCipherString(word, codebook)

    if codeword is not None:
        if not word.isalnum():
            word = re.sub(r'[a-zA-Z0-9]+', codeword, word) #maintain punctuation and decode nomenclator
        else:
            word = codeword

    return word

#encrypt word accodring to key
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

#decrypt word according to key
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


#see if word is nomenclator
def searchPlainString(word: str, codebook: dict):
    word = re.sub(r'[^A-Z]', '', word)
    for codeword, codenumbers in codebook.items():
        if word == codeword:
            return codenumbers
                
    return None

#see if word nomenclator
def searchCipherString(word: str, codebook: dict):
    word = re.sub(r'[^0-9]', '', word)
    for codename, code_list in codebook.items():
        if word in code_list:
            return codename

    return None


def test():
    pass
    


if __name__ == '__main__':
    test()