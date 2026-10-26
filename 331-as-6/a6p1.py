#!/usr/bin/env python3

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
Problem 1
"""

from sys import flags
from collections import Counter

def getOccurences(text, n ):
    engram_list = [text[i:i+n] for i in range(0, len(text), n)]

    if len(engram_list) % n != 0:
        engram_list.append(text[-1 * n - 1:])

    engram_count = len(engram_list)

    return engram_count, engram_list


def ngramsFreqs(text: str, n: int) -> dict[str, float]:
    """
    text: the content string
    n: the size of the n-grams
    """
    if text == "":
        return {}
    if n == 0:
        return {text: 1}
    if n < 0:
        raise ValueError("n cannot be negative")
    if n > len(text):
        raise ValueError("n cannot be larger than text")
    
    engram_dict = {}
    engram_count, engram_list = getOccurences(text, n)

    engram_dict = {engram: count / engram_count for engram, count in Counter(engram_list).items()}

    for key, value in engram_dict.items():
        print(key, value)
    
    return engram_dict
    

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

if __name__ == "__main__" and not flags.interactive:
    test()
