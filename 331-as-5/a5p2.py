#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 10/17/26 Chris Scheerschmidt
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
CMPUT 331 Assignment 5 Problem 2 Student Solution
Author: Chris Scheerschmidt
"""

from sys import flags
def pretty_close(array_one, array_two):
    if len(array_one) != len(array_two):
        return False
    for i in range(len(array_one)):
        if abs(array_one[i] - array_two[i]) > 0.00001:
            return False
    return True

def evalDecipherment(text1: str, text2: str) -> list[float]:
    """
    text1 is a plaintext and text2 is an attempted decipherment of a
    ciphertext created by enciphering text1.

    This function should compare the two files and return a list containing two fields that
    correspond to the key accuracy and decipherment accuracy of text2 w.r.t. the plaintext, text1
    """
    lettercount = 0
    matchcount = 0
    textletters = set()
    matchletters = set()

    for plainchar, cipherchar in zip(list(text1), list(text2)):
        if plainchar.isalpha():
            plainchar = plainchar.upper()
            textletters.add(plainchar)
            lettercount += 1

            if cipherchar.isalpha():
                cipherchar = cipherchar.upper()

                if plainchar == cipherchar:
                    matchcount += 1
                    matchletters.add(plainchar)

    if len(matchletters) == 0 and len(textletters) == 0:
        return [0.0, 0.0]
    
    keyaccuracy = len(matchletters) / len(textletters)
    deciperaccuracy = matchcount / lettercount

    return [keyaccuracy, deciperaccuracy]


def test():
    pass
    
    
if __name__ == '__main__' and not flags.interactive:
    test()
