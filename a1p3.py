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
CMPUT 331 Assignment 1 Student Solution
September 2026
Author: Chris Scheerschmidt
"""

import re
from sys import flags
from a1p1 import encrypt, decrypt

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def crack_caesar(ciphertext: str, val_words: set) -> str:
    plaintext = ""
    plainlist = []
    matchlist = []
    matches = 0
    firstwords = []
    bestmatch = ""
    firstalpha = ""

    for letter in LETTERS:
        plaintext = decrypt(ciphertext, letter) 
        plainlist = re.sub(r'[^A-Z\s]', '', plaintext).split()
        firstwords.append(plainlist[0])

        for word in plainlist:
            if word in val_words:
                matches += 1

        matchlist.append(matches)
        matches = 0

    #get decryption with most matches
    #test if more than one decryption with this many matches
    #select decryption with plaintext that comes first alphabetically
    maxval = max(matchlist)
    for i, val in enumerate(matchlist):
         if val == maxval:
              if not firstalpha or firstwords[i] < firstalpha:
                   bestmatch = LETTERS[i]
                   
    return decrypt(ciphertext , bestmatch), bestmatch

def form_dictionary(text_address='carroll-alice.txt') -> set:
    word_set = set()

    with open(text_address, 'r', encoding = 'utf-8') as f:
        word_set.update(re.sub(r'[^A-Z\s]', '', f.read().upper()).split())

    return word_set

def test():
        sample = "Throughout the unusually quiet afternoon, several researchers gathered inside an old observatory to examine a collection of documents discovered beneath the foundation of a recently renovated building. Although the papers initially appeared to contain nothing more than ordinary notes, receipts, diagrams, and incomplete calculations, a closer examination revealed that many of the pages had been deliberately rearranged. Some paragraphs ended abruptly, while others began with sentences that seemed to belong somewhere else entirely. The researchers therefore decided to catalogue every document before attempting to determine how the pieces were connected. Each page received a unique identification number, and its physical characteristics were recorded alongside the visible text. Pages containing similar handwriting were grouped together, while fragments with unusual markings were temporarily placed in a separate collection. As the investigation continued, several recurring phrases appeared throughout the documents. These phrases were particularly interesting because they occurred in locations where ordinary sentences would not normally contain repeated expressions. One researcher suggested that the repetition might indicate an encrypted message, while another believed that the patterns were simply a consequence of the author's unusual writing style. To distinguish between these possibilities, the researchers entered the text into a computer program capable of testing numerous substitution patterns. The program systematically transformed each character according to a predetermined mathematical relationship and then compared the resulting text against a dictionary of known words. At first, most transformations produced meaningless combinations of letters. However, one particular transformation produced several recognizable words in succession. The discovery encouraged the researchers to examine the remaining passages more carefully. They found that the same transformation worked on multiple documents, suggesting that the unusual arrangement of the pages had not been accidental. Further examination revealed references to locations, dates, measurements, and instructions concerning a device that had apparently been constructed many decades earlier. The device itself was nowhere to be found, but descriptions of its components appeared repeatedly in the surviving documents. According to the notes, the mechanism consisted of several rotating disks connected to a complicated system of gears. Changing the position of one disk altered the relationship between the other disks, creating a sequence of transformations that could be used to encode written messages. The researchers were particularly interested in determining whether the mechanism had been designed for practical communication or merely as an intellectual experiment. Unfortunately, many of the most important pages were damaged beyond recognition, leaving significant gaps in the historical record. Nevertheless, the surviving evidence provided enough information to reconstruct several portions of the original system. By comparing the repeated terminology, numerical values, and descriptions of the mechanism, the researchers gradually developed a consistent explanation for how the device had operated. Their reconstruction was not perfect, but subsequent experiments demonstrated that the proposed mechanism could reproduce the transformations described in the documents. What had initially seemed to be a collection of unrelated papers therefore became evidence of a carefully designed cryptographic system. The discovery raised additional questions about who had created the system, why it had been abandoned, and whether other examples of the same technique might still exist. Further research was planned, including a detailed examination of archives, private collections, and historical records associated with the building. Although the investigation would require considerable time, the researchers believed that the remaining evidence could eventually provide a more complete understanding of the mysterious documents and the unusual machine described within them."
        key = "Z"
        cracked, key = crack_caesar(encrypt(sample, key), form_dictionary())
        print(cracked, key)

if __name__ == "__main__" and not flags.interactive:
    test()