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

#generate list of random numbers of size n according to algorithm Ri+2 = a*R1+1 + bRi + c (mod m)
#list consists of elements R2, R3, ..., R1+n
def random_generator(a, b, c, m, r0, r1, n):
    randlist = [0] * n
    rand = 0
    for i in range(0, n):
        rand = ( (a * r1) + (b * r0) + c ) % m
        randlist[i] = rand
        r0 = r1
        r1 = rand
        
    return randlist

def test():
    pass

if __name__ == "__main__" and not flags.interactive:
    test()
