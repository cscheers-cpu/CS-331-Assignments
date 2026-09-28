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


def insertBlanks(key: List[int], plaintext: list[str], blanks: int, rows: int) -> list:
    cutoff = len(key) - blanks
    counter = 0
    insertion = rows - 1
    while counter <= blanks:
        if key[counter] > cutoff:
            plaintext.insert(insertion, None)
        counter = counter + 1
        insertion = insertion + rows

    return plaintext


def decipherMessage(key: List[int], message: str) -> str:
    plaintext = list(message)
    plainstring = ""
    rows = len(message) // len(key)
    if len(message) % len(key) > 0:
        rows = rows + 1

    blankspaces = len(key) * rows - len(message)
    if blankspaces > 0:
        plaintext = insertBlanks(key, plaintext, blankspaces, rows)

    #make seperate function
    for row in range(rows):
        for column in range(1, len(key) + 1):
            column = key.index(column)
            index = (column * rows) + row
            letter = plaintext[index]

            if letter is None:
                continue
            else:
                plainstring = plainstring + letter

    return plainstring




def test():
    pass

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
