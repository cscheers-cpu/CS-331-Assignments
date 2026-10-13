#!/usr/bin/env python3


#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 10/8/2026 Chris Scheerschmidt
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
Enhanced substitution cipher solver
Author: Chris Scheerschmidt
"""
from __future__ import annotations

import re
import simpleSubHacker as ssh

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class wordMatches:
    def __init__(self,
            cipherword: str, 
            plainword: str,  
            formatword: str, 
            plainindices: list[int],  
            formatindices: list[int], 
            wordmatches: list[str] | None = None):
        
        self.cipherword = cipherword
        self.plainword = plainword
        self.formatword = formatword
        self.formatindices = formatindices
        self.plainindices = plainindices
        self.wordmatches = wordmatches if wordmatches is not None else []
        
    def get_cipherword(self):
        return self.cipherword
    
    def get_plainword(self):
        return self.plainword

    def get_formatword(self):
        return self.formatword
    
    def get_plainindices(self):
        return self.plainindices

    def get_formatindices(self):
        return self.formatindices

    def get_wordmatches(self):
        return self.wordmatches

    def set_wordmatches(self, wordmatches: list[str]):
        self.wordmatches = wordmatches

    def len_wordmatches(self) -> int:
        return len(self.wordmatches)


def loadDictionary(file: str) -> set[str]:
    dict = set()
    with open(file) as f:
        for word in f.read().split('\n'):
            dict.add(word)
    return dict

def getUnmatchedLetters(mapping: dict[str, list[str]]) -> set[str]: 
    unmatchedletters: set[str] = set()
    for plainletters in mapping.values():
        if len(plainletters) > 1:
            unmatchedletters.update(plainletters)

    return unmatchedletters

#cipherword = key, value = getMatches object
def getIncompleteWordDict(plaintext: str, ciphertext: str, regexletters: str) -> dict[str, wordMatches]:
    incompletedict = {}
    plainindices: list[int] = []

    plaintextlist = plaintext.split()
    cipherlist = ciphertext.split()

    for index, word in enumerate(plaintextlist):
        if '_' in word:
            if cipherlist[index] not in incompletedict:
                formatted_word, formatted_indices = getFormattedWord(word, regexletters)
                plainindices = [i for i, char in enumerate(word) if char == '_']
                incompletedict[cipherlist[index]] = wordMatches(cipherlist[index], word, formatted_word, plainindices, formatted_indices) #incomplete word = key, tuple(cipherword, []) = value. empty list to hold indices of '_'
            else:
                pass

    return incompletedict

def getFormattedWord(word: str, regexletters:str) -> tuple[str, list[int]]:
    temp_word = word.upper()

    #check if contraction
    if "'" in temp_word and temp_word[-1] != "'":
        temp_word = re.sub(r"[^A-Z_']", "", temp_word)

    else:
        temp_word = re.sub(r"[^A-Z_]", "", temp_word)
        #check if plural
        if temp_word[-1] == 'S':
                temp_word = temp_word + '?'
        else:
            pass

    format_indices = [i for i, char in enumerate(temp_word) if char == '_']
    temp_word = '^' + re.sub('_', regexletters, temp_word) + '$'
    
    return temp_word, format_indices


def getMatches(incompletedict: dict[str, wordMatches], contractiondict: set[str], standarddict: set[str], regexletters:str) -> dict[str, wordMatches]:
    for matchobject in incompletedict.values():
        matches = []
        #search dictionary for word

        temp_word = matchobject.get_formatword()

        if "'" in temp_word:
            matches = [d_word for d_word in contractiondict if re.search(temp_word, d_word)]

        elif len(temp_word) == 1:
            print("here")
            if 'A' in regexletters:
                matches.append('A')
            if 'I' in regexletters:
                matches.append('I')
            if 'O' in regexletters:
                matches.append('O')
        else:
            matchone = [d_word for d_word in contractiondict if re.search(temp_word, d_word)]
            matchtwo = [d_word for d_word in standarddict if re.search(temp_word, d_word)]
            for match in matchtwo:
                if match not in matchone:
                    matchone.append(match)
            matches = matchone

        matchobject.set_wordmatches(matches)

    return incompletedict


"""
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
"""
def hackSimpleSub(message: str):
    standarddict = loadDictionary('dictionary.txt')
    contractiondict = loadDictionary('english_contractions.txt')
    newmapping: dict[str, list[str]] = {}
    mapping: dict[str, list[str]] = ssh.hackSimpleSub(message)
    unmatchedletters = getUnmatchedLetters(mapping)
    regexletters = '[' + ''.join(unmatchedletters) + ']'

    plaintext: str = ssh.decryptWithCipherletterMapping(message, mapping)
    incompletedict = getIncompleteWordDict(plaintext, message, regexletters)

    incompletedict = getMatches(incompletedict, contractiondict, standarddict, regexletters)
    incompletelist: list[wordMatches] = [value for value in incompletedict.values() if value.len_wordmatches() > 0]

    incompletelist.sort(key=lambda obj: obj.len_wordmatches(), reverse=True)
    
    for thing in reversed(incompletelist):
        print(thing.get_plainword())
        print(thing.get_wordmatches())
        print()



    """  for item in incompletedict.values():
        cipherword = item.get_cipherword()
        plainword = item.get_plainword()
        formatword = item.get_formatword()
        plainindices =  item.get_plainindices()
        formatindices = item.get_formatindices()
        wordmatches = item.get_wordmatches()
        print(cipherword)
        print(plainword)
        print(formatword)
        print(plainindices)
        print(formatindices)
        print(wordmatches)
        print()"""

    print(plaintext)
    plaintext = ssh.decryptWithCipherletterMapping(message, mapping)
    print(plaintext)


    return plaintext

    


def test():
    # Provided test.
    """
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
        assert(hackSimpleSub(message)=="If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell")
        messageone = 'Cug zlxtq pfwdk iwv hlseo wmgf cug rjyn awb, plc cug awb, pgxkb mgfn cxfga jicgf j rwkb jicgfkwwk wi tujoxkb ozlxffgro cufwlbu cug bjfagk, oxsern njdkga jka dgkc pjtq cw orgge. Sgjkduxrg, cug iwv cfwccga efwlarn jtfwoo cug sgjawd, ergjoga dxcu xco osjrr mxtcwfn. Kwpwan kwcxtga, wi twlfog; cug ijfsgf djo plon fgejxfxkb cug wra igktg kgjf cug fxmgf.'
        solution = 'The quick brown fox jumps over the lazy dog, but the dog, being very tired after a long afternoon of chasing squirrels through the garden, simply yawned and went back to sleep. Meanwhile, the fox trotted proudly across the meadow, pleased with its small victory. Nobody noticed, of course; the farmer was busy repairing the old fence near the river.'
    """
    messageone = 'Cug zlxtq pfwdk iwv hlseo wmgf cug rjyn awb, plc cug awb, pgxkb mgfn cxfga jicgf j rwkb jicgfkwwk wi tujoxkb ozlxffgro cufwlbu cug bjfagk, oxsern njdkga jka dgkc pjtq cw orgge. Sgjkduxrg, cug iwv cfwccga efwlarn jtfwoo cug sgjawd, ergjoga dxcu xco osjrr mxtcwfn. Kwpwan kwcxtga, wi twlfog; cug ijfsgf djo plon fgejxfxkb cug wra igktg kgjf cug fxmgf.'
    solution =  'The quick brown fox jumps over the lazy dog, but the dog, being very tired after a long afternoon of chasing squirrels through the garden, simply yawned and went back to sleep. Meanwhile, the fox trotted proudly across the meadow, pleased with its small victory. Nobody noticed, of course; the farmer was busy repairing the old fence near the river.'
    assert(hackSimpleSub(messageone)) == solution
if __name__ == '__main__':
    test()


"""for i, j in zip(indextuple[0], indextuple[1]):
                print(i)
                plainletter = match[j]
                cipherletter = cipherword[i].upper()
                print(plainletter, cipherletter)
                print()
                mapping[cipherletter] = [plainletter]"""