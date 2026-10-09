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

def encipherMessage(key: int, message: str) -> str:
    ciphertext = ""
    rows = len(message) // key
    if (len(message) % key > 0):
        rows = rows + 1

    for column in range(key): #iter through rows (vertical axes)
        for row in range(rows): #iter through columns (horizontal axes)
            index = column + (row * key) #jump to next column and maintain row
            if index > len(message) - 1: #break if leftover blankspaces reached
                break
            ciphertext = ciphertext + message[index]
    
    return ciphertext

def insertBlanks(newmessage: list, blanks: int, key: int, columns: int):
    for i in range(blanks, 0, -1):
        ind = columns * (key - i) + columns - 1
        newmessage.insert(ind, None)

    return newmessage

def decipherMessage(key: int, message: str) -> str:
    plaintext = ""
    columns = len(message) // key
    newmessage: list[str | None] = list(message)

    if (len(message) % key > 0):
        columns = columns + 1
        blanks = columns * key - len(message)
        newmessage = insertBlanks(newmessage, blanks, key, columns)

    #same logic as encipherMessage except row, column length swapped
    for column in range(columns): 
        for row in range(key):
            index = column + (row * columns) 
            if index > len(newmessage) - 1: 
                break

            letter = newmessage[index]
            if letter is not None:
                plaintext = plaintext + letter
            else:
                pass

    return plaintext



def test():
    pass

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
