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

def get_lcm (a: int, b: int):
    gcd_ab = math.gcd(a,b)
    coprime_a = a // gcd_ab
    coprime_b = b // gcd_ab
    print(coprime_a, coprime_b)
    return coprime_a, coprime_b

def remove_b(cgone1: list[int], cgone2: list[int]):
    coprime1, coprime2 = get_lcm(cgone1[2], cgone2[2])
    bgone = [0] * 2
    for i in range(2):
        bgone[i] = cgone1[i] * coprime2 - cgone2[i] * coprime1
    print(bgone)
    return bgone

def isolate_a (int, r4: list[int], r5: list[int], r6: list[int]):
    cgone1 = [r4[0] - r5[0], r4[1] - r5[1], r4[2] - r5[2]] #cgone = R4 - R5
    cgone2 = [r5[0] - r6[0], r5[1] - r6[1], r5[2] - r6[2]]
    print(cgone1)
    print(cgone2)
    remove_b(cgone1, cgone2)




def crack_rng(m: int, sequence: list[int]):
    aisolate = list[int]
    r4: list[int] = [sequence[2], sequence[1], sequence[0]]
    r5: list[int] = [sequence[3], sequence[2], sequence[1]]
    r6: list[int] = [sequence[4], sequence[3], sequence[2]]

    aisolate = isolate_a(m, r4, r5, r6)
    


    
    


def test():
    assert crack_rng(17, [14, 13, 16, 3, 13]) == [3, 5, 9]


if __name__ == "__main__" and not flags.interactive:
    test()
