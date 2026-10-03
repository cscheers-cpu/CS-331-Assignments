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
    coprime_a = a/gcd_ab
    coprime_b = b/gcd_ab
    return coprime_a, coprime_b

def isolate_a (m: int, eq1, eq2, eq3):



def crack_rng(m: int, sequence: list[int]):
    r4: tuple = (sequence[0], sequence[1])
    r5: tuple = (sequence[1], sequence[2])
    r5: tuple = (sequence[2], sequence[3])
    


def test():
    assert crack_rng(17, [14, 13, 16, 3, 13]) == [3, 5, 9]


if __name__ == "__main__" and not flags.interactive:
    test()
