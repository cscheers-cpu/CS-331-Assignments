#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright <<Insert the date here>> <<Insert your name here>>
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
CMPUT 331 Assignment 5 Problem 2 Student Solution
Author: <Your name here>
"""

from sys import flags

def pretty_close(array_one, array_two):
    if len(array_one) != len(array_two):
        return False
    for i in range(len(array_one)):
        if abs(array_one[i] - array_two[i]) > 0.00001:
            return False
    return True

def evalDecipherment(text1: str, text2: str) -> [float, float]:
    """
    text1 is a plaintext and text2 is an attempted decipherment of a
    ciphertext created by enciphering text1.

    This function should compare the two files and return a list containing two fields that
    correspond to the key accuracy and decipherment accuracy of text2 w.r.t. the plaintext, text1
    """
    raise NotImplementedError()


def test():
    "Run tests"
    assert pretty_close(evalDecipherment("this is an example", "tsih ih an ezample") , [0.7272727272727273, 0.7333333333333333])
    assert pretty_close(evalDecipherment("the most beautiful course is 331!", "tpq munt bqautiful cuurnq in 331!") , [0.7142857142857143, 0.625])
    
    
if __name__ == '__main__' and not flags.interactive:
    test()
