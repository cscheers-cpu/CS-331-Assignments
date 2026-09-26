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
    raise NotImplementedError()

def decipherMessage(key: int, message: str) -> str:
    raise NotImplementedError()

def test():
    assert encipherMessage(5, "CIPHERS ARE FUN") == "CREIS P FHAUERN"
    assert decipherMessage(2, encipherMessage(2, "SECRET")) == "SECRET"
    assert decipherMessage(3, encipherMessage(3, "CIPHERS ARE FUN")) == "CIPHERS ARE FUN"
    assert decipherMessage(4, encipherMessage(4, "HELLO WORLD")) == "HELLO WORLD"

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
