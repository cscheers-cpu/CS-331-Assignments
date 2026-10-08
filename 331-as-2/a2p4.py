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
CMPUT 331 Assignment 2 Student Solution
September 2026
Author: Chris Scheerschmidt
"""

from typing import List
from itertools import permutations
from a2p3 import decipherMessage

def crackSharedKey(keylength: int, cipherWords: List[str]) -> list[list[int]]: 
    dict = form_dictionary()
    keyperms = getKeys(keylength)
    keymatches = [0] * len(keyperms)
    goodkeys: list[list[int]] = []

    for word in cipherWords: #iter through given cipherwords
        for j, perm in enumerate(keyperms): #iter through possible key permutations, save index of each permutation
            plaintext = decipherMessage(perm, word) #decipher word with current key permutation

            #if deciphered word is actual word, increment permutation match counter
            if plaintext in dict: 
                keymatches[j] = keymatches[j] + 1 #

    #save key permutations that work for every cipherword
    for i, matches in enumerate(keymatches):
        if matches == len(cipherWords):
            goodkeys.append(keyperms[i])

    return goodkeys

#generate all permutations of keys given keylength
def getKeys(keylength:int) -> list[list[int]] :
    genlist = [0] * keylength
    for i in range(1, keylength + 1):
        genlist[i-1] = i

    return [list(p) for p in permutations(genlist)]

#save words in dictionary.txt to set
def form_dictionary(text_address='dictionary.txt') -> set[str]:
    dict = set()
    with open(text_address, 'r', encoding = 'utf-8') as f:
        dict = {line.rstrip('\n') for line in f}

    return dict

def test():
    assert crackSharedKey(3, ['AET', 'WSA', 'OSM']) == [], 'a2p4.crackSharedKey test 1'
    assert crackSharedKey(3, ['AET', 'WSA']) == [[1, 3, 2]], 'a2p4.crackSharedKey test 2'
    assert crackSharedKey(3, ['AET']) == [[1, 3, 2], [2, 1, 3], [3, 2, 1]], 'a2p4.crackSharedKey test 3'
    assert crackSharedKey(3, ['WSA']) == [[1, 3, 2], [3, 1, 2]], 'a2p4.crackSharedKey test 4'
    assert crackSharedKey(3, ['WSA', 'RILCAET']) == [[1, 3, 2]], 'a2p4.crackSharedKey test 5'
    assert crackSharedKey(3, ['WEUNAHSGROI', 'DIEOINNUSGUS', 'SFNNFGUI', 'NARETGO', 'OPUUTT']) == [[1, 2, 3]], 'a2p4.crackSharedKey test 6'
    assert crackSharedKey(3, ['KGWIAN', 'BUNENILG', 'RFFTYOI', 'OSPRTOE', 'BWRDNUO', 'CANEATGSLI', 'CCIROINENLG', 'CNLHIE', 'OBISPHIORITN']) == [[3, 1, 2]], 'a2p4.crackSharedKey test 7'
    assert crackSharedKey(5, ['EDWSLI', 'NNTSICSAO', 'UHTLGOY', 'IEEENDSVC']) == [[3, 5, 1, 4, 2]], 'a2p4.crackSharedKey test 8'
    assert crackSharedKey(2, ['CUCLONI', 'OFRFES', 'WCYAK', 'SMOEUMND', 'CEMRA', 'DCEEKD', 'MRSAE', 'ARTDEAE', 'ABBA', 'SRMEGTOBR']) == [[1, 2]], 'a2p4.crackSharedKey test 9'
    assert crackSharedKey(4, ['LNRAXY', 'HEOODT', 'MERSATK', 'SAMDUNMS', 'MGLANI', 'GTAISN', 'BSDOE', 'VETESO']) == [[1, 3, 2, 4]], 'a2p4.crackSharedKey test 10'
    assert crackSharedKey(4, ['RAXLNY', 'OODHET', 'RSATMEK', 'MDUNSAMS', 'LANMGI', 'AISGTN', 'DOBSE', 'GNNIAREG']) == [[3, 2, 1, 4]], 'a2p4.crackSharedKey test 11'
    assert crackSharedKey(5, ['TAEBTIN', 'ILLXAECPBNIE', 'COOGRONYHL']) == [[1, 4, 3, 5, 2]], 'a2p4.crackSharedKey test 12'
    assert crackSharedKey(5, ['TINBTAE', 'PBNIEECILLXA', 'UETFDLA']) == [[5, 2, 3, 1, 4]], 'a2p4.crackSharedKey test 13'
    assert crackSharedKey(4, ['ELSNIT', 'TSLEIN', 'PPHYA']) == [[4, 3, 1, 2]], 'a2p4.crackSharedKey test 14'
    assert crackSharedKey(3, ['OUSCPEMT', 'ECCDOAMRY', 'OTPTCNRRUEAS', 'IASNSGL']) == [[2, 1, 3]], 'a2p4.crackSharedKey test 15'
    assert crackSharedKey(6, ['ATECRRE', 'URDHLE']) == [[2, 3, 4, 1, 5, 6]], 'a2p4.crackSharedKey test 16'
    assert crackSharedKey(4, ['RRNBSOTSEO', 'HGLXNEOAA', 'UUARSN']) == [[1, 3, 2, 4]], 'a2p4.crackSharedKey test 17'
    assert crackSharedKey(4, ['BSEORRNOTS', 'XNAAHGLEO', 'DREDCWOO']) == [[3, 4, 1, 2]], 'a2p4.crackSharedKey test 18'
    assert crackSharedKey(4, ['EOBSRRNOTS', 'AAXNHGLEO', 'EDDRCWOO']) == [[4, 3, 1, 2]], 'a2p4.crackSharedKey test 19'
    assert crackSharedKey(4, ['OTSRRNEOBS', 'EOHGLAAXN', 'OESCRU']) == [[2, 1, 4, 3]], 'a2p4.crackSharedKey test 20'
    


from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
