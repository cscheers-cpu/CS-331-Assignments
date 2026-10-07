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

def encipherMessage(key: List[int], message: str) -> str:
    ciphertext = ""
    columns = len(message) // len(key)
    if len(message) % len(key) > 0:
        columns = columns + 1

    for row in key: #iter through rows (vertical axes)
        row = row - 1 #convert row to index
        for column in range(columns): #iter through columns (horizontal axes)
            index = row + (len(key) * column) #jump to next column and maintain row
            if index > len(message) - 1:
                continue
            ciphertext = ciphertext + message[index]

    return ciphertext


def test():
    pass
    
from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
