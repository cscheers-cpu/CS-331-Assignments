#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright <<Insert the date here>> <<Insert your name here>>
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
CMPUT 331 Assignment 5 Problem 3 Student Solution
Author: <Your name here>
"""
import a5p1, a5p2
from sys import flags

def checkLetterFrequency(ciphertext: str) -> dict:
    ciphertext = ciphertext.upper()
    #keep only alpha

    #count total # letters

    #count each letter
    frequency = {}

    for char in letters:
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1

    for char in frequency:

    return frequency
    raise NotImplementedError


def test():
    assert checkLetterFrequency("ABCD") == {"A" : 0.25, "B" : 0.25, "C" : 0.25, "D" : 0.25}

if __name__ == '__main__' and not flags.interactive:
    test()
