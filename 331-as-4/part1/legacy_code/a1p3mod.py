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
#          gkondrak <at> ualberta.ca
#
#---------------------------------------------------------------

"""
CMPUT 331 Assignment 1 Student Solution
September 2026
Author: Chris Scheerschmidt
"""

#use module re for string formatting
import re
from sys import flags
from legacy_code.a1p1mod import encrypt, decrypt

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def crack_caesar(ciphertext: str, val_words: dict) -> tuple[str, str]:
    #store message 
    #store formatted message as list of CAPITALIZED WORDS
    plaintext = ""
    plainlist = []

    #number of words in message that were found in dict (per key)
    #list storing number of matches per key tested
    #letter key that best fits based on assignment specs
    matches = 0
    matchlist = []
    bestmatch = ""

    #holds first word of message for case testing
    #list holding first word of each keys decryption output
    firstalpha = ""
    firstwords = []

    for letter in LETTERS:
        plaintext = decrypt(ciphertext, letter) 

        #remove all non-letters or spaces, store each word in string in list
        plainlist = re.sub(r'[^A-Z\s]', '', plaintext).split()

        #add first word of this decryption attempt to list = firstwords 
        firstwords.append(plainlist[0])

        #count number of valid words found in message
        #add number of matches to list
        for word in plainlist:
            if word in val_words:
                matches += 1

        matchlist.append(matches)
        matches = 0

    #find largest number of matches
    #check if other decryption keys produce same number of matches
    #if more than one key with maxval matches, choose based on plaintext alphabetically
    maxval = max(matchlist)
    for i, val in enumerate(matchlist):
         if val == maxval:
              if not firstalpha or firstwords[i] < firstalpha:
                   bestmatch = LETTERS[i]
                   
    return decrypt(ciphertext , bestmatch), bestmatch

def form_dictionary(text_address='carroll-alice.txt') -> set:
    word_set = set()

    #open 'carroll-alice.txt, copy text into one large string using f.read()
    #capitalize all letters, remove all non characters and spaces, store each word in set = word_set
    with open(text_address, 'r', encoding = 'utf-8') as f:
        for line in f:
             word_set.add(line.rstrip("\n"))
    return word_set

def test():
        pass

if __name__ == "__main__" and not flags.interactive:
    test()