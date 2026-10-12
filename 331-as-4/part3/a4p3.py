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
Enhanced substitution cipher solver
Author: Chris Scheerschmidt
"""
from __future__ import annotations

import re
import simpleSubHacker as ssh

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def loadDictionary(file: str) -> set[str]:
    with open(file) as f:
        englishWords = set()
        for word in f.read().split('\n'):
            englishWords.add(word)
    return englishWords

def getUnmatchedLetters(mapping: dict[str, list[str]]) -> set[str]: 
    unmatchedletters: set[str] = set()
    for plainletters in mapping.values():
        if len(plainletters) > 1:
            unmatchedletters.update(plainletters)

    return unmatchedletters

def getIncompleteWordDict(plaintext: str, ciphertext: str) -> dict[str, tuple[str, list[int], list[int]]]:
    incompletedict: dict[str, tuple[str, list[int], list[int]]] = {}
    plaintextlist = plaintext.split()
    cipherlist = ciphertext.split()

    for index, word in enumerate(plaintextlist):
        if '_' in word:
            if word not in incompletedict:
                incompletedict.update({word: (cipherlist[index], [], [])}) #incomplete word = key, tuple(cipherword, []) = value. empty list to hold indices of '_'
            else:
                pass


    return incompletedict



"""
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
"""
def hackSimpleSub(message: str):
    standarddict = loadDictionary('dictionary.txt')
    contractiondict = loadDictionary('english_contractions.txt')

    print(standarddict)

    mapping: dict[str, list[str]] = ssh.hackSimpleSub(message)
    unmatchedletters = getUnmatchedLetters(mapping)
    regexletters = '[' + ''.join(unmatchedletters) + ']'

    plaintext: str = ssh.decryptWithCipherletterMapping(message, mapping)
    incompletedict = getIncompleteWordDict(plaintext, message)

    regexletters = ""
    temp_word = ""

    #iter through unknown words and their plaintext indices
    for word, tuple in incompletedict.items():
        temp_word = word.upper()
        tuple[1].extend([i for i, char in enumerate(word) if char == '_'])

        #if word plural, make 'S' optional so dictionary will still identify if plural not in dictionary
        #replace all non char elements in word
        #THINK OF OTHER CASES
        #all indices = indices of where '_' occur in single word
        if temp_word[-1] == 'S':
            temp_word = temp_word + '?'
            temp_word = re.sub(r"[^A-Z_?]", "", temp_word)
            tuple[2].extend([i for i, char in enumerate(temp_word) if char == '_']) #index

        #handle contractions ('re, 'nt, etc)
        elif "'" in temp_word:
            apostindex = temp_word.find("'")
            temp_word = temp_word[0:apostindex]
            tuple[2].extend([i for i, char in enumerate(temp_word) if char == '_']) #index 
            temp_word = re.sub(r"[^A-Z_]", "", temp_word)

        #standard word
        else:
           temp_word = re.sub(r"[^A-Z_]", "", temp_word)
           tuple[2].extend([i for i, char in enumerate(temp_word) if char == '_']) #index 

        #convert string to regex, eg. insert [ABCD] at '_'
        temp_word = '^' + re.sub('_', regexletters, temp_word) + '$'


        #search dictionary for word
        match = next((d_word for d_word in standarddict if re.search(temp_word, d_word)), None)


        if match is not None:
            for i, j in zip(tuple[1], tuple[2]):
                print(i)
                plainletter = match[j]
                cipherletter = tuple[0][i].upper()
                print(plainletter, cipherletter)
                print()
                mapping[cipherletter] = [plainletter]


    
    print(mapping)
             
    plaintext = ssh.decryptWithCipherletterMapping(message, mapping)

    print(plaintext)



    return plaintext

    


def test():
    # Provided test.
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    hackSimpleSub(message)
    assert(hackSimpleSub(message)=="If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell")
    # End of provided test.
    

if __name__ == '__main__':
    test()
