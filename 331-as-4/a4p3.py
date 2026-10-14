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
from pathlib import Path
from collections import defaultdict

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 

#load dictionary from .txt
def loadDictionary(filepath) -> set[str]:
    dict = set()
    with open(filepath) as f:
        for word in f.read().split('\n'):
            dict.add(word)
    return dict
CONTRACTIONDICT = loadDictionary(Path(__file__).parent / 'dictionaries' /'english_contractions.txt')
STANDARDDICT = loadDictionary(Path(__file__).parent / 'dictionaries' /'dictionary.txt')

"""
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
"""
def hackSimpleSub(message: str):
    origmessage = message #save copy of original cipher

    message = re.sub(r"[^a-zA-Z_']", " ", message)
    mapping = ssh.hackSimpleSub(message)

    unmatchedletters = getUnmatchedLetters(mapping)
    matchedletters = set(letter for letter in LETTERS if letter not in unmatchedletters)
    regexletters = '[' + ''.join(unmatchedletters) + ']'

    #decipher, store all words with '_' in incomplete dict
    plaintext = ssh.decryptWithCipherletterMapping(message, mapping)
    incompletedict = getIncompleteWordDict(plaintext, message, regexletters)

    #search through dictionaries for possible words, store in incomplete dict, wordMatches object
    incompletedict = getMatches(incompletedict, regexletters)
    incompletelist: list[wordMatch] = [value for value in incompletedict.values() if value.len_wordMatch() > 0] #eliminate words with no word matches

    #sort wordMatch objects in list based on number of wordmatches per plainword
    incompletelist.sort(key=lambda obj: obj.len_wordMatch()) 
    listbylength = [list(group) for key, group in groupby(incompletelist, key=lambda obj: obj.len_wordMatch())]

    #find mapped letters, update mapping, update ciphertext, find mapped letters, ... until all words have been matched
    counter = 0
    while listbylength:
        counter += 1
        listbylength, mapping = recursiveUpdate(listbylength, mapping,matchedletters, message)
        if counter == 200:
            break

    return ssh.decryptWithCipherletterMapping(origmessage, mapping)


#find inital unmatched letters in deciphered message
def getUnmatchedLetters(mapping: dict[str, list[str]]) -> set[str]: 
    unmatchedletters: set[str] = set()
    for plainletters in mapping.values():
        if len(plainletters) > 1:
            unmatchedletters.update(plainletters)

    return unmatchedletters


#make dictionary of incomplete words in plaintext
#cipherword is key, wordMatch object is value
def getIncompleteWordDict(plaintext: str, ciphertext: str, regexletters: str) -> dict[str, wordMatch]:
    incompletedict = {}
    plainindices = []

    plaintextlist = plaintext.split()
    cipherlist = ciphertext.split()

    #eliminate whitespace after hyphen elimination
    plaintextlist = [split_word for word in plaintextlist for split_word in word.split()]
    cipherlist = [split_word for word in cipherlist for split_word in word.split()]

    #make dict
    for plainword, cipherword in zip(plaintextlist, cipherlist):
        if '_' in plainword:
            if cipherword not in incompletedict:
                formatted_word, formatted_indices = getFormattedWord(plainword, regexletters)
                plainindices = [i for i, char in enumerate(plainword) if char == '_']
                incompletedict[cipherword] = wordMatch(cipherword, plainword, formatted_word, plainindices, formatted_indices) 

    return incompletedict


#format plainword with regex sequence
#regex sequence is all unmatched letters
def getFormattedWord(word: str, regexletters:str) -> tuple[str, list[int]]:
    word = word.upper()
    word = re.sub(r"^'+|'+$", "", word)

    if word and word[-1] == 'S':
            word = word + '?'

    format_indices = [i for i, char in enumerate(word) if char == '_']    #make list of indices of '_'
    word = '^' + re.sub('_', regexletters, word) + '$'
    
    return word, format_indices


#search through dictionaries for possible words given plaintext word
def getMatches(incompletedict: dict[str, wordMatch], regexletters:str) -> dict[str, wordMatch]:
    for matchobject in incompletedict.values():
        plainword = matchobject.get_plainword()
        matches = []
        temp_word = matchobject.get_formatword()

        if "'" in temp_word:
            matches = [d_word for d_word in CONTRACTIONDICT if re.search(temp_word, d_word)]

        elif len(plainword) == 1:
            if 'A' in regexletters:
                matches.append('A')
            if 'I' in regexletters:
                matches.append('I')
            if 'O' in regexletters:
                matches.append('O')
        else:
            #search both contraction dict for slang and given dict. combine elements into one list
            matchlistone = [d_word for d_word in CONTRACTIONDICT if re.search(temp_word, d_word)]
            matchlisttwo = [d_word for d_word in STANDARDDICT if re.search(temp_word, d_word)]

            for match in matchlisttwo:
                if match not in matchlistone:
                    matchlistone.append(match)
            matches = matchlistone

        matchobject.set_wordMatch(matches)

    return incompletedict


#go through list of wordMatch objects
#determine which letters can be mapped based on dictionary hits
#all wordMatches in list have same number of possible dicionary words
#logic works because these have smallest possble matched dict words (if we find a matched letter here, must be THE letter)
def getPossibleLetterCombos(matchlist: list[wordMatch], mapping: dict[str, list[str]], matchedletters):
    possibleletters = {}

    for matchobject in matchlist:
        cipherword:str = matchobject.get_cipherword()
        cipherindices: list[int] = matchobject.get_plainindices()
        matchindices: list[int] = matchobject.get_formatindices()
        numindices: int = matchobject.len_indices()
        wordmatches: list[str] = matchobject.get_wordMatch()
        checkmatches  = defaultdict(set)                       

        for word in wordmatches:
            for i in range(numindices):
                cipherletter = cipherword[cipherindices[i]].upper()
                matchletter = word[matchindices[i]]

                checkmatches.setdefault(cipherletter, set()).add(matchletter)
                possibleletters.setdefault(cipherletter, set()).add(matchletter)

        #if n letters have been matched, and there n indices, these must be the letters
        for cipherletter, matchletterset in checkmatches.items():
            if len(matchletterset) == 1:
                char = next(iter(matchletterset))
                mapping[cipherletter] = [char]
                matchedletters.add(char)

    #if out of all words that have been checked, there is a letter that has only been mapped once, this must be the letter
    for cipherletter, matchletters in possibleletters.items():
        if len(matchletters) == 1:
            char = next(iter(matchletters))
            mapping[cipherletter] = [char]
            matchedletters.add(char)

    return mapping, matchedletters


#find mapped letters, update mapping, update ciphertext, find mapped letters, ... until all words have been matched
def recursiveUpdate(listbylength, mapping, matchedletters, message):
    mapping, matchedletters = getPossibleLetterCombos(listbylength[0], mapping, matchedletters) #match plain letters to cipher letters based on words found in dictionaries
    matchedletters, mapping = updateMatchedLetters(matchedletters, mapping) #update mapping given new matched letters

    plaintext = ssh.decryptWithCipherletterMapping(message, mapping) #update plaintext

    #update unmatchedletters, regexletters
    unmatchedletters = [letter for letter in LETTERS if letter not in matchedletters]
    regexletters = '[' + ''.join(unmatchedletters) + ']'

    #update dict
    incompletedict = getIncompleteWordDict(plaintext, message, regexletters)
    incompletedict = getMatches(incompletedict, regexletters)

    #sort list of wordMatches
    incompletelist: list[wordMatch] = [value for value in incompletedict.values() if value.len_wordMatch() > 0]
    incompletelist.sort(key=lambda obj: obj.len_wordMatch())

    return [list(group) for key, group in groupby(incompletelist, key=lambda obj: obj.len_wordMatch())], mapping


#update mapping until matched letters have been removed from all values
def updateMatchedLetters(matchedletters, mapping):
    check = True
    while check:
        check = False
        prematchedletters = matchedletters.copy()
        for value in mapping.values():
            if len(value) > 1:
                for letter in value:
                    if letter in matchedletters:
                        value.remove(letter)

                        #if after updating, current value has only one element, add it to matchedletters
                        if len(value) == 1:
                            matchedletters.add(value[0])

        #once we iterate through values and matchedletters has not been appended, we have removed matched letters from all unmatched cipher, plailetter combos            
        if matchedletters > prematchedletters:
            check = True

    return matchedletters, mapping

        
        
def test():
    pass

    

if __name__ == '__main__':
    test()


