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
    word = re.sub(r'[\n\t\r]', ' ', word)
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

    escape_sequences = r'\\[ntrvfb0]'
    cipherlist = [""] * len(messagelist)
    
    for i, word in enumerate(messagelist):
        if re.search(escape_sequences, word):
            esclist = re.split(r'(\\.)', word)
            word = applyEscape(esclist, escape_sequences, codebook, key, 'encrypt')
           
        else:
            word = testEncryptWord(word, codebook, key)

        cipherlist[i] = word

    plaintext = ''. join(cipherlist)
    
    plaintext = plaintext.encode('utf-8').decode('unicode_escape')
    
    return plaintext


def testEncryptWord(word, codebook, key):
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

    return encryptWord(word, key)


def testDecryptWord(word, codebook, key):
    word = decryptWord(word, key)
    codeword = searchCipherString(word, codebook)

    if codeword is not None:
        if not word.isalnum():
            word = re.sub(r'^([^a-zA-Z0-9]*)[a-zA-Z0-9]+([^a-zA-Z0-9]*)$', rf'\1{codeword}\2', word)
        else:
            word = codeword

    return word


def applyEscape(esclist, escsequences, codebook, key, mode):
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

    escape_sequences = r'\\[ntrvfb0]'
    plaintextlist = [""] * len(messagelist)

    for i, word in enumerate(messagelist):
        if  re.search(escape_sequences, word):
            esclist = re.split(r'(\\.)', word)
            word = applyEscape(esclist, escape_sequences, codebook, key, 'decrypt')
        else:
            word = testDecryptWord(word, codebook, key)

        plaintextlist[i] = word

    plaintext = ''. join(plaintextlist)
    plaintext = plaintext.encode('utf-8').decode('unicode_escape')
    
    return plaintext
        


    escape_sequences = r"[\n\t\r\0\v\f\b]|\S+"
    messagelist = re.findall(escape_sequences, message)


def test():


    # 1. assignment example
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'university': ['1', '2', '3'], 'examination': ['4', '5'], 'examinations': ['6', '7', '8'], 'WINTER': ['9']}
    plaintext = 'At the University of Alberta, examinations take place in December and April for the Fall and Winter terms.'
    ciphertext = 'Lj jia 2 py Lmfacjl, 7 jlka bmlwa sx Oawanfac lxo Lbcsm ypc jia Ylmm lxo 9 jacnr.'
    expected = 'At the university of Alberta, examinations take place in December and April for the Fall and WINTER terms.'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected

    # 2. no codebook words
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'university': ['1', '2', '3'], 'examination': ['4', '5'], 'examinations': ['6', '7', '8'], 'WINTER': ['9']}
    plaintext = 'Hello, world! This message has nothing from the codebook.'
    ciphertext = 'Iammp, epcmo! Jisr narrlua ilr xpjisxu ycpn jia wpoafppk.'
    expected = 'Hello, world! This message has nothing from the codebook.'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 3. empty codebook
    key = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    codebook = {}
    plaintext = 'Nothing here is replaced; only letters change.'
    ciphertext = 'Fgziofu itkt ol kthsqetr; gfsn stzztkl eiqfut.'
    expected = 'Nothing here is replaced; only letters change.'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 4. empty message
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'university': ['1', '2', '3'], 'examination': ['4', '5'], 'examinations': ['6', '7', '8'], 'WINTER': ['9']}
    plaintext = ''
    ciphertext = ''
    expected = ''
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 5. reverse key
    key = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    codebook = {}
    plaintext = 'Zebra crossing: a quick test.'
    ciphertext = 'Avyiz xilhhrmt: z jfrxp gvhg.'
    expected = 'Zebra crossing: a quick test.'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 6. single symbols
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'the': ['10'], 'and': ['11'], 'hello': ['12'], 'Cat': ['13'], 'dogs': ['14']}
    plaintext = 'The cat and the dogs said hello.'
    ciphertext = '10 13 11 10 14 rlso 12.'
    expected = 'the Cat and the dogs said hello.'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 7. case-insensitive codebook
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'hello': ['5']}
    plaintext = 'HELLO Hello hello hElLo'
    ciphertext = '5 5 5 5'
    expected = 'hello hello hello hello'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 8. punctuation around codebook words
    key = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    codebook = {'hello': ['1', '2']}
    plaintext = '"hello" hello; (hello) hello... hello?'
    ciphertext = '"2" 1; (2) 1... 1?'
    expected = '"hello" hello; (hello) hello... hello?'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected

    # 9. mixed case non-codebook
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {}
    plaintext = 'HeLLo wOrLD, SoMeThInG StRaNgE'
    ciphertext = 'IaMMp ePcMO, RpNaJiSxU RjClXuA'
    expected = 'HeLLo wOrLD, SoMeThInG StRaNgE'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 10. codebook key with capitals
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'WINTER': ['9']}
    plaintext = 'winter Winter WINTER wInTeR'
    ciphertext = '9 9 9 9'
    expected = 'WINTER WINTER WINTER WINTER'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 11. adjacent punctuation
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'wait': ['0']}
    plaintext = "Wait... what?! Yes -- really; (maybe), 'sure'."
    ciphertext = "0... eilj?! Har -- calmmh; (nlhfa), 'rtca'."
    expected = "wait... what?! Yes -- really; (maybe), 'sure'."
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 12. digits in message
    key = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    codebook = {'cats': ['40'], 'dogs': ['41']}
    plaintext = 'In 2003 there were 5 cats and 12 dogs.'
    ciphertext = 'Of 2003 zitkt vtkt 5 40 qfr 12 41.'
    expected = 'In 2003 there were 5 cats and 12 dogs.'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected
    assert encryptMessage(key, plaintext, codebook) == ciphertext

    # 13. multi-digit symbols
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'the': ['100', '101'], 'cat': ['7'], 'and': ['25'], 'dogs': ['300']}
    plaintext = 'the cat and the dogs'
    ciphertext = '101 7 25 100 300'
    expected = 'the cat and the dogs'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected

    # 14. plural vs singular entries
    key = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    codebook = {'university': ['1', '2', '3'], 'examination': ['4', '5'], 'examinations': ['6', '7', '8'], 'WINTER': ['9']}
    plaintext = 'examination examinations examination'
    ciphertext = '5 7 4'
    expected = 'examination examinations examination'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected

    # 15. long text all words in codebook
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    codebook = {'the': ['1', '2', '3'], 'and': ['4', '5']}
    plaintext = 'the and the and'
    ciphertext = '1 4 2 5'
    expected = 'the and the and'
    assert decryptMessage(key, ciphertext, codebook) == expected
    assert decryptMessage(key, encryptMessage(key, plaintext, codebook), codebook) == expected

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

"""            word = decryptWord(word, key)
            codeword = searchCipherString(word, codebook)

            if codeword is not None:
                if not word.isalnum():
                    word = re.sub(r'^([^a-zA-Z0-9]*)[a-zA-Z0-9]+([^a-zA-Z0-9]*)$', rf'\1{codeword}\2', word)
                else:
                    word = codeword"""