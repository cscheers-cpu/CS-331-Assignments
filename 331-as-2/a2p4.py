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
CMPUT 331 Assignment 2 Student Solution
September 2026
Author: Chris Scheerschmidt
"""

from typing import List
from itertools import permutations
from a2p3 import decipherMessage

def crackSharedKey(keylength: int, cipherWords: List[str]): 
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        pass

def form_dictionary(text_address='dictionary.txt') -> set:
    word_set = set()
    with open(text_address, 'r', encoding = 'utf-8') as f:
        for line in f:
            word_set.update(line.strip())

    return word_set

def test():
    assert len(crackSharedKey(3, ["AET"])) == 3 # [[1, 3, 2], [2, 1, 3], [3, 2, 1]]
    assert len(crackSharedKey(3, ["WSA"])) == 2 # [[1, 3, 2], [3, 1, 2]]
    assert len(crackSharedKey(3, ["AET", "WSA"])) ==  1 # [[1, 3, 2]]
    assert len(crackSharedKey(3, ["AET", "WSA", "OSM"])) == 0 # []

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
