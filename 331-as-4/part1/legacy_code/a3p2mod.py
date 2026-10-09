#!/usr/bin/python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 10/3/2026 Chris Scheerschmidt
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
# ---------------------------------------------------------------

"""
CMPUT 331 Assignment 3 Student Solution
Author: Chris Scheerschmidt
"""

from sys import flags
import math

#find possible affine cypher key pairings given modulus
#do not count case where a = 1, b = 0 (result is same cypher-alphabet as plain-alphabet)
def affine_key_count(m):
    if m == 1 or m == 0:
        return 0
    
    count = 0
    for i in range(1, m):
        if math.gcd(i, m) == 1:
            count = count + 1
    return count * m - 1

def test():
    pass


if __name__ == "__main__" and not flags.interactive:
    test()
