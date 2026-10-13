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
import helper_functions.simpleSubHacker as ssh
from itertools import groupby
from helper_functions.wordMatch import wordMatch

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 

def loadDictionary(file: str) -> set[str]:
    dict = set()
    with open(file) as f:
        for word in f.read().split('\n'):
            dict.add(word)
    return dict

def getUnmatchedLetters(mapping: dict[str, list[str]]) -> set[str]: 
    unmatchedletters: set[str] = set()
    for plainletters in mapping.values():
        if len(plainletters) > 1:
            unmatchedletters.update(plainletters)

    return unmatchedletters

#cipherword = key, value = getMatches object
def getIncompleteWordDict(plaintext: str, ciphertext: str, regexletters: str) -> dict[str, wordMatch]:
    incompletedict = {}
    plainindices: list[int] = []
    plaintextlist = []
    cipherlist = []

    plaintextlist = plaintext.split()
    cipherlist = ciphertext.split()


    plaintextlist = [re.sub(r"\b.-\b|\b-.|(?<=\w)-(?=\w)", ' ', word) for word in plaintextlist]
    cipherlist = [re.sub(r"\b.-\b|\b-.|(?<=\w)-(?=\w)", ' ', word) for word in cipherlist]

    plaintextlist = [split_word for word in plaintextlist for split_word in word.split()]
    cipherlist = [split_word for word in cipherlist for split_word in word.split()]

    for index, word in enumerate(plaintextlist):
        if '_' in word:
            if cipherlist[index] not in incompletedict:
                formatted_word, formatted_indices = getFormattedWord(word, regexletters)
                plainindices = [i for i, char in enumerate(word) if char == '_']
                incompletedict[cipherlist[index]] = wordMatch(cipherlist[index], word, formatted_word, plainindices, formatted_indices) #incomplete word = key, tuple(cipherword, []) = value. empty list to hold indices of '_'
            else:
                pass

    return incompletedict

def getFormattedWord(word: str, regexletters:str) -> tuple[str, list[int]]:
    temp_word = word.upper()

    if "'" in temp_word and temp_word[-1] != "'":
        temp_word = re.sub(r"[^A-Z_']", "", temp_word)

    else:
        temp_word = re.sub(r"[^A-Z_]", "", temp_word)
        #check if plural
        if temp_word[-1] == 'S':
                temp_word = temp_word + '?'
        else:
            pass

    format_indices = [i for i, char in enumerate(temp_word) if char == '_']
    temp_word = '^' + re.sub('_', regexletters, temp_word) + '$'
    
    return temp_word, format_indices


def getMatches(incompletedict: dict[str, wordMatch], contractiondict: set[str], standarddict: set[str], regexletters:str) -> dict[str, wordMatch]:
    for matchobject in incompletedict.values():
        matches = []
        #search dictionary for word

        temp_word = matchobject.get_formatword()

        if "'" in temp_word:
            matches = [d_word for d_word in contractiondict if re.search(temp_word, d_word)]

        elif len(temp_word) == 1:
            if 'A' in regexletters:
                matches.append('A')
            if 'I' in regexletters:
                matches.append('I')
            if 'O' in regexletters:
                matches.append('O')
        else:
            matchone = [d_word for d_word in contractiondict if re.search(temp_word, d_word)]
            matchtwo = [d_word for d_word in standarddict if re.search(temp_word, d_word)]
            for match in matchtwo:
                if match not in matchone:
                    matchone.append(match)
            matches = matchone

        matchobject.set_wordMatch(matches)

    return incompletedict


def getPossibleLetterCombos(matchlist: list[wordMatch], mapping: dict[str, list[str]], matchedletters):
    possibleletters = {}
    for thing in matchlist:
        cipherword = thing.get_cipherword()
        cipherindices = thing.get_plainindices()
        matchindices = thing.get_formatindices()
        numindices = thing.len_indices()
        checkmatches = set()
        
        for word in thing.get_wordMatch():
            for i in range(numindices):
                cipherindex = cipherindices[i]
                cipherletter = cipherword[cipherindex].upper()

                matchindex = matchindices[i]
                matchletter = word[matchindex]
                checkmatches.add(matchletter)
                if cipherletter not in possibleletters:
                    possibleletters.update({cipherletter: set()})
                    possibleletters[cipherletter].add(matchletter)
                else:
                    possibleletters[cipherletter].add(matchletter)
            
        if len(checkmatches) == numindices:
            for i in range(numindices):
                cipherindex = cipherindices[i]
                cipherletter = cipherword[cipherindex].upper()

                matchindex = matchindices[i]
                matchletter = thing.get_wordMatch()[0][matchindex]
                mapping[cipherletter] = [matchletter]
                matchedletters.add(matchletter)
                    


            


    for cipherletter, matchletters in possibleletters.items():
        if len(matchletters) == 1:
            char = next(iter(matchletters))
            mapping[cipherletter] = [char]
            matchedletters.add(char)

    return mapping, matchedletters


"""
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
"""
def hackSimpleSub(message: str):
    origmessage = message
    standarddict = loadDictionary('dictionary.txt')
    contractiondict = loadDictionary('english_contractions.txt')

    message = re.sub(r"[^a-zA-Z_']", " ", message)
    mapping: dict[str, list[str]] = ssh.hackSimpleSub(message)


    unmatchedletters = getUnmatchedLetters(mapping)
    matchedletters = set(letter for letter in LETTERS if letter not in unmatchedletters)
    regexletters = '[' + ''.join(unmatchedletters) + ']'

    plaintext: str = ssh.decryptWithCipherletterMapping(message, mapping)
    """    plaintext = re.sub(r"[^a-zA-Z_']", " ", plaintext)
    scrubbedciphertext = re.sub(r"[^a-zA-Z_']", " ", message)"""

    print(plaintext)
    print()
    print(message)

    incompletedict = getIncompleteWordDict(plaintext, message, regexletters)
   

    incompletedict = getMatches(incompletedict, contractiondict, standarddict, regexletters)
    incompletelist: list[wordMatch] = [value for value in incompletedict.values() if value.len_wordMatch() > 0]
    print()


    incompletelist.sort(key=lambda obj: obj.len_wordMatch())
    listbylength = [list(group) for key, group in groupby(incompletelist, key=lambda obj: obj.len_wordMatch())]
    print(incompletedict)
    print(listbylength[0])

    while listbylength:
        mapping, matchedletters = getPossibleLetterCombos(listbylength[0], mapping, matchedletters)

        check = True
        while check:
            check = False
            prematchedletters = matchedletters
            for value in mapping.values():
                if len(value) > 1:
                    for letter in value:
                        if letter in matchedletters:
                            value.remove(letter)

                            if len(value) == 1:
                                matchedletters.add(value[0])
            if matchedletters > prematchedletters:
                check = True
            
        plaintext = ssh.decryptWithCipherletterMapping(message, mapping)

        unmatchedletters = [letter for letter in LETTERS if letter not in matchedletters]
        regexletters = '[' + ''.join(unmatchedletters) + ']'

        incompletedict = getIncompleteWordDict(plaintext, message, regexletters)
        incompletedict = getMatches(incompletedict, contractiondict, standarddict, regexletters)

        incompletelist: list[wordMatch] = [value for value in incompletedict.values() if value.len_wordMatch() > 0]
        incompletelist.sort(key=lambda obj: obj.len_wordMatch())

        listbylength = [list(group) for key, group in groupby(incompletelist, key=lambda obj: obj.len_wordMatch())]


    return ssh.decryptWithCipherletterMapping(origmessage, mapping)

        
   
#for words with '-' in them, split at '-'
def test():
    pass

    #messageten = '''Zjp lqz xqz ed zjp nqz. Zjp lqz xqu zjp hqz. Zjp hqz hqd oqxz zjp nqz, qdf zjp lqz hqd qszph zjp hqz, qdf zjqz uqx zjqz.'''
    #solutionten = '''The cat sat on the mat. The cat saw the rat. The rat ran past the mat, and the cat ran after the rat, and that was that.'''
    #assert hackSimpleSub(messageten) == solutionten
    





if __name__ == '__main__':
    test()


