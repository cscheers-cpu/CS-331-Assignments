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

#inserts None at points in list plaintext where blankspaces would be
def insertBlanks(key: List[int], plaintext: list[str | None], blanks: int, rows: int) -> list:
    cutoff = len(key) - blanks #blanks will be in rows with largest values, stop at some smaller value
    counter = 0
    insertionpoint = rows - 1 #initial insertion point, will be at bottom of row
    while counter <= blanks:
        if key[counter] > cutoff: #check if current row is large enough
            plaintext.insert(insertionpoint, None)
        counter = counter + 1
        insertionpoint = insertionpoint + rows #jump to botom of next row

    return plaintext


def decipherMessage(key: List[int], message: str) -> str:
    plainlist: list[str | None] = list(message)
    plainstring = ""
    rows = len(message) // len(key)
    if len(message) % len(key) > 0:
        rows = rows + 1

    #if blankspaces present, pad list with None at their coordinates
    blankspaces = len(key) * rows - len(message)
    if blankspaces > 0:
        plainlist = insertBlanks(key, plainlist, blankspaces, rows)

    for row in range(rows): #iter through rows (vertical axis)
        for column in range(1, len(key) + 1): #iter through column values
            column = key.index(column) #get index of column from key
            index = (column * rows) + row #jump between columns while maintaining row
            letter = plainlist[index]

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
