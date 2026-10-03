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

def remove_constant(m: int, equ1: list[int], equ2: list[int]):
    coprime1, coprime2 = get_lcm(equ1[2], equ2[2])
    constgone = [0] * 2
    for i in range(2):
        constgone[i] = (equ1[i] * coprime2 - equ2[i] * coprime1) % m
    print(constgone)
    
    return constgone

def apply_modinverse(m: int, isolate: list[int]):
    inversex = pow(isolate[1], -1, m)
    x = (isolate[0] * inversex) % m

    return x

    
def find_ab (m: int, r4: list[int], r5: list[int], r6: list[int]):
    a = 0
    b = 0
    bgone = [0] * 2
    acgone = [0] * 2
    cgone1 = [r4[0] - r5[0], r4[1] - r5[1], r4[2] - r5[2]] #cgone = R4 - R5
    cgone2 = [r5[0] - r6[0], r5[1] - r6[1], r5[2] - r6[2]]
    print(cgone1)
    print(cgone2)
    bgone = remove_constant(m, cgone1, cgone2)
    print(bgone)
    a = apply_modinverse(m, bgone)
    print(a)
    print()
    print("-" * 20)
    print()
    print(cgone1[0])
    print(cgone1[1])
    acgone[0] = (cgone1[0] - cgone1[1] * a) % m
    acgone[1] = cgone1[2]
    print(acgone)
    b = apply_modinverse(m, acgone)
    print(b)
    

    return a, b

    



def crack_rng(m: int, sequence: list[int]):
    inversea = 0
    constgone = [0] * 2
    r4: list[int] = [sequence[2], sequence[1], sequence[0]]
    r5: list[int] = [sequence[3], sequence[2], sequence[1]]
    r6: list[int] = [sequence[4], sequence[3], sequence[2]]

    a, b = find_ab(m, r4, r5, r6)
    #sub a for each equation
    r4[1] = r4[1] * a
    r5[1] = r5[1] * a
    r6[1] = r6[1] * a




    
    


def test():
    assert crack_rng(17, [14, 13, 16, 3, 13]) == [3, 5, 9]


if __name__ == "__main__" and not flags.interactive:
    test()
