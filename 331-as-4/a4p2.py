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


"""def translateMessage(key: str, message: str, codebook: dict, mode: str):
    
    Encrypt or decrypt using a nomenclator.
    Takes a substitution cipher key, a message (plaintext or ciphertext),
    a codebook dictionary, and a mode string ('encrypt' or 'decrypt')
    specifying the action to be taken. Returns a string containing the
    ciphertext (if encrypting) or plaintext (if decrypting).
    
    raise NotImplementedError()"""

def searchPlainString(word: str, codebook: dict):
    word = re.sub(r'[\n\t\r]', ' ',)
    word = re.sub(r'[^A-Z]', '', word)
    for codeword, codenumbers in codebook.items():
        if word == codeword:
            return codenumbers
                
    return None


def searchCipherString(word: str, codebook: dict):
    word = re.sub(r'[^0-9]', '', word)
    for codename, code_list in codebook.items():
        if word in code_list:
            return codename

    return None


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
    codebook = {codeword.upper(): codenumbers for codeword, codenumbers in codebook.items()}

    escape_sequences = r"(\\[ntr0vfdwsbWDSB])"
    message = message.encode('unicode_escape').decode('utf-8')
    messagelist = re.split(escape_sequences, message)
    messagelist = [word for word in messagelist if word != '']
    print(messagelist)
    cipherlist = [""] * len(messagelist)
    codenumbers = []
    

    for i, word in enumerate(messagelist):
        codenumbers = searchPlainString(word.upper(), codebook)

        if codenumbers is not None:
            number = random.choice(codenumbers)
            if not word.isalnum():
                temp_word = re.search(r"[a-zA-Z0-9].*[a-zA-Z0-9]|[a-zA-Z0-9]", word)
                if temp_word:
                    temp_word = temp_word.group()
                    word = re.sub(temp_word, number, word)
            else:
                word = number

        cipherlist[i] = encryptWord(word, key)

    return " ".join(cipherlist)

def applyEscape(esclist, escsequences, codebook, key):
    newlist = [""] * len(esclist)

    for i, word in enumerate(esclist):
        if re.search(escsequences, word):
            newlist[i] = word
        else:
            word = decryptWord(word, key)
            codeword = searchCipherString(word, codebook)

            if codeword is not None:
                if not word.isalnum():
                    word = re.sub(r'^([^a-zA-Z0-9]*)[a-zA-Z0-9]+([^a-zA-Z0-9]*)$', rf'\1{codeword}\2', word)
                else:
                    word = codeword
            newlist[i] = word

    return ''.join(newlist)
            


def decryptMessage(key: str, message: str, codebook: dict):
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

    print(messagelist)
    escape_sequences = r'\\[ntrvfb0]'
    plaintextlist = [""] * len(messagelist)
    codeword = ""

    for i, word in enumerate(messagelist):
        if  re.search(escape_sequences, word):
            print(word)
            esclist = re.split(r'(\\.)', word)
            word = applyEscape(esclist, escape_sequences, codebook, key)
            print(word)
        else:
            word = decryptWord(word, key)
            codeword = searchCipherString(word, codebook)

            if codeword is not None:
                if not word.isalnum():
                    word = re.sub(r'^([^a-zA-Z0-9]*)[a-zA-Z0-9]+([^a-zA-Z0-9]*)$', rf'\1{codeword}\2', word)
                else:
                    word = codeword

        plaintextlist[i] = word

    plaintext = ''. join(plaintextlist)
    plaintext = plaintext.encode('utf-8').decode('unicode_escape')
    return plaintext
        


    escape_sequences = r"[\n\t\r\0\v\f\b]|\S+"
    messagelist = re.findall(escape_sequences, message)


def test():
    # 16. newlines and spacing
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'cat': ['9']}
    plaintext = 'Line one has the cat.\nLine two,  with  double spaces\tand a tab.'
    ciphertext = 'Msxa pxa ilr jia 9.\nMsxa jep,  esji  optfma rblwar\tlxo l jlf.'
    expected = 'Line one has the cat.\nLine two,  with  double spaces\tand a tab.'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    print('all Problem 2 asserts passed')


    # End of provided tests.

if __name__ == '__main__':
    test()
    """   key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
        plaintext = "X-ray machines cannot be brought here, as -ray* are very dangerous. Hello;ray! ray;"
        codebook = {'ray':['1']}
        ciphertext = encryptMessage(key, plaintext, codebook)
        print(decryptMessage(key, ciphertext, codebook ))
        assert ciphertext =="G-clh nlwisxar wlxxpj fa fcptuij iaca, lr -1* lca qach olxuacptr. Iammp;clh! 1;"""
    # Provided tests.
 

""" if char.isalpha():
            temp_char = char.upper()
            char_index = CHAR_TO_INDEX[char]
            if char.isupper():
                ciphertext[i] = temp_char
            else:
                ciphertext[i] = temp_char.lower()"""