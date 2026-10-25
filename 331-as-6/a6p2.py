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

TEST_ENCODE = {'O': 'G',   'Y': 'L',   'K': 'E',   'M': 'W',   'S': 'C',   'Z': 'Y',   'A': 'Z', 
            
            'D': 'S',   'B': 'J',   'U': 'Q',   'Q': 'N',   'F': 'V',   'L': 'M',   'J': 'B', 

            'C': 'K',    'W': 'F',  'N': 'O',   'H': 'T',    'E': 'I',   'I': 'R',  'P': 'A', 

            'G': 'P',   'X': 'U',   'V': 'D',   'T': 'X',    'R': 'H',  ' ': ' '
}

TEST_DECODE = {'G': 'O',    'L': 'Y',   'E': 'K',   'W': 'M',   'C': 'S',   'Y': 'Z',   'Z': 'A', 
               
               'S': 'D',     'J': 'B',   'Q': 'U',  'N': 'Q',   'V': 'F',   'M': 'L',    'B': 'J', 

               'K': 'C',    'F': 'W',    'O': 'N',  'T': 'H',   'I': 'E',    'R': 'I',   'A': 'P', 

               'P': 'G',    'U': 'X',    'D': 'V',   'X': 'T',  'H': 'R',   ' ': ' '}

TEST_TEXTS = [
    "EEFFFEEF",

    "HELLO WORLD",

    "ABCABCABC",

    "AAAA AAAA",

    "THE QUICK BROWN FOX",

    "ATTACK AT DAWN",

    "CRYPTOGRAPHY IS FUN",

    "A B C D E",

    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",

    "HELLO HELLO HELLO",

    "MISSISSIPPI RIVER",

    "AB AB AB AB",

    "  A  B  C  ",

    "SPACE SPACE SPACE",

    "COMPUTER SCIENCE",

    "ENIGMA MACHINE",

    "Z",

    "",
]

TEST_CIPHERS = ['IIVVVIIV',
                 
                'TIMMG FGHMS', 

                'ZJKZJKZJK', 

                'ZZZZ ZZZZ', 

                'XTI NQRKE JHGFO VGU', 

                'ZXXZKE ZX SZFO',

                'KHLAXGPHZATL RC VQO',

                'Z J K S I', 

                'ZJKSIVPTRBEMWOGANHCXQDFULY', 

                'TIMMG TIMMG TIMMG', 

                'WRCCRCCRAAR HRDIH',

                'ZJ ZJ ZJ ZJ',

                '  Z  J  K  ', 

                'CAZKI CAZKI CAZKI', 

                'KGWAQXIH CKRIOKI',

                'IORPWZ WZKTROI', 

                'Y', 

                ''
        ]

from sys import flags
import random
from a6p1 import ngramsFreqs

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

    alpha_encode = dict(zip(keys, values))
    alpha_encode.update({' ': ' '})

    alpha_decode = dict(zip(values, keys))
    alpha_decode.update({' ': ' '})


    return alpha_encode, alpha_decode

def encipher(mapping = TEST_ENCODE, plaintext = ''):
    cap_text = plaintext.upper()
    encipher_list = [""] * len(plaintext)

    for i in range(0, len(plaintext)):
        char = mapping[cap_text[i]]

        if plaintext[i].islower():
            encipher_list[i] = char.lower()
        elif plaintext[i].isupper():
            encipher_list[i] = char
        else:
            encipher_list[i] = plaintext[i]

    return ''.join(encipher_list)


def decipher(mapping = TEST_DECODE, ciphertext = ''):
    cap_text = ciphertext.upper()
    decipher_list = [""] * len(ciphertext)

    for i in range(0, len(ciphertext)):
        char = mapping[cap_text[i]]

        if ciphertext[i].islower():
            decipher_list[i] = char.lower()
        elif ciphertext[i].isupper():
            decipher_list[i] = char
        else:
            decipher_list[i] = ciphertext[i]

    return ''.join(decipher_list)


def keyScore(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> float:
    plaintext = decipher(mapping, ciphertext)
    testfreqs = ngramsFreqs(plaintext, n)

    realengrams = frequencies.keys()


    for engram, testfreq in testfreqs.items():
        if engram in realengrams:
            realfreq = frequencies[engram]
            
        pass

    pass
  

def test():
    test_deciphers = [encipher(TEST_ENCODE, text) for text in TEST_TEXTS]
    print(test_deciphers)
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

if __name__ == "__main__" and not flags.interactive:
    test()





