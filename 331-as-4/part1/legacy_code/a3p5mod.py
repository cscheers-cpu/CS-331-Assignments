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

#get lcm of two integers
def get_lcm (a: int, b: int):
    gcd_ab = math.gcd(a,b)
    coprime_a = a // gcd_ab
    coprime_b = b // gcd_ab

    return coprime_a, coprime_b

#isolate a given two equations with c eliminated (eliminate b)
def isolate_a(m: int, cgone1: list[int], cgone2: list[int]):
    bgone = [0] * 2
    coprime1, coprime2 = get_lcm(cgone1[2], cgone2[2])

    bgone[0] = (cgone1[0] * coprime2 - cgone2[0] * coprime1) % m
    bgone[1] = (cgone1[1] * coprime2 - cgone2[1] * coprime1) % m
    
    return bgone

#isolate b given 3 equations with c eliminated and by substituting a
#consider possibilty of only 1 equation having non-zero b value
def isolate_b(m:int, a: int, cgone1: list[int], cgone2: list[int], cgone3: list[int]):
    acgone = [0] * 2
    
    if cgone1[2] != 0:
        acgone[0] = (cgone1[0] - cgone1[1] * a) % m
        acgone[1] = cgone1[2]

    elif cgone2[2] != 0:
          acgone[0] = (cgone2[0] - cgone2[1] * a) % m
          acgone[1] = cgone2[2]
    else:
          acgone[0] = (cgone3[0] - cgone3[1] * a) % m
          acgone[1] = cgone3[2]       

    return acgone

#apply modular inverse to find a/b
def apply_modinverse(m: int, equality: list[int]):
    inversex = pow(equality[1], -1, m)
    x = (equality[0] * inversex) % m

    return x


def crack_rng(m: int, sequence: list[int]):
    a: int = 0
    b: int = 0
    c: int = 0
    bcgone: list[int] = [0] * 2
    acgone: list[int] = [0] * 2

    r4: list[int] = [sequence[2], sequence[1], sequence[0]]
    r5: list[int] = [sequence[3], sequence[2], sequence[1]]
    r6: list[int] = [sequence[4], sequence[3], sequence[2]]

    #isolate c using all possible combos in case b = 0 for cgone1[2] and cgone2[2]
    cgone1 = [r4[0] - r5[0], r4[1] - r5[1], r4[2] - r5[2]] #R4 - R5
    cgone2 = [r5[0] - r6[0], r5[1] - r6[1], r5[2] - r6[2]] #R5 - R6
    cgone3 = [r4[0] - r6[0], r4[1] - r6[1], r4[2] - r6[2]] #R4 - R6

    bcgone = isolate_a(m, cgone1, cgone2)
    a = apply_modinverse(m, bcgone)

    acgone = isolate_b(m, a, cgone1, cgone2, cgone3)
    b = apply_modinverse(m, acgone)

    c = (r4[0] - r4[1] * a - r4[2] * b) % m

    return [a, b, c]

def test():
    pass


if __name__ == "__main__" and not flags.interactive:
    test()
