#!/usr/bin/env python3

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
Problem 2
"""
ALPHABET = ['A', 
            'B',
            'C',
            'D',
            'E', 
            'F', 
            'G', 
            'H', 
            'I', 
            'J', 
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z'
        ]

TEST_MAP = {'O': 'A',   'I': 'J',   'U': 'T',   'N': 'L',   'Q': 'M',   'B': 'F', 
            
            'V': 'P',   'E': 'V',   'D': 'H',   'M': 'X',   'L': 'O',   'Y': 'D', 

            'J': 'B',   'C': 'R',   'F': 'G',   'Z': 'C',   'W': 'E',   'K': 'Z', 

            'X': 'W', 'T': 'U', 'S': 'Q', 'A': 'K', 'H': 'I', 'P': 'N', 'G': 'S', 

            'R': 'Y', ' ': ' '
        }

from sys import flags
import random

#generate random character mapping
def get_mapping():
    self_map = True
    keys = []
    values = []

    while self_map:
        self_map = False
        keys = random.sample(ALPHABET, len(ALPHABET))
        values = random.sample(ALPHABET, len(ALPHABET))

        for key_letter, value_letter in zip(keys, values):
            if key_letter == value_letter:
                self_map = True
                break

    alpha_dict = dict(zip(keys, values))
    alpha_dict.update({' ': ' '})

    return alpha_dict


def keyScore(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> float:
    raise NotImplementedError()
  

def test():
    print(get_mapping())
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

if __name__ == "__main__" and not flags.interactive:
    test()





