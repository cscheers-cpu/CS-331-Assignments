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
import helper_functions.simpleSubHacker as ssh
from itertools import groupby
from helper_functions.wordMatch import wordMatch
from pathlib import Path
from collections import defaultdict

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 

#load dictionary from .txt
def loadDictionary(filepath) -> set[str]:
    dict = set()
    with open(filepath) as f:
        for word in f.read().split('\n'):
            dict.add(word)
    return dict
CONTRACTIONDICT = loadDictionary(Path(__file__).parent / 'dictionaries' /'english_contractions.txt')
STANDARDDICT = loadDictionary(Path(__file__).parent / 'dictionaries' /'dictionary.txt')

"""
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
"""
def hackSimpleSub(message: str):
    origmessage = message #save copy of original cipher

    message = re.sub(r"[^a-zA-Z_']", " ", message) # remove all symbols from cipher except characters, '_' and "'"
    mapping = ssh.hackSimpleSub(message)

    unmatchedletters = getUnmatchedLetters(mapping)
    matchedletters = set(letter for letter in LETTERS if letter not in unmatchedletters)
    regexletters = '[' + ''.join(unmatchedletters) + ']'

    #decipher, store all words with '_' in incomplete dict
    plaintext = ssh.decryptWithCipherletterMapping(message, mapping)
    incompletedict = getIncompleteWordDict(plaintext, message, regexletters)

    #search through dictionaries for possible words, store in incomplete dict, wordMatches object
    incompletedict = getMatches(incompletedict, regexletters)
    incompletelist: list[wordMatch] = [value for value in incompletedict.values() if value.len_wordMatch() > 0] #eliminate words with no word matches

    #sort wordMatch objects in list based on number of wordmatches per plainword
    incompletelist.sort(key=lambda obj: obj.len_wordMatch()) 
    listbylength = [list(group) for key, group in groupby(incompletelist, key=lambda obj: obj.len_wordMatch())]

    #find mapped letters, update mapping, update ciphertext, find mapped letters, ... until all words have been matched
    while listbylength:
        listbylength, mapping = recursiveUpdate(listbylength, mapping, matchedletters, message)


    return ssh.decryptWithCipherletterMapping(origmessage, mapping)


#find inital unmatched letters in deciphered message
def getUnmatchedLetters(mapping: dict[str, list[str]]) -> set[str]: 
    unmatchedletters: set[str] = set()
    for plainletters in mapping.values():
        if len(plainletters) > 1:
            unmatchedletters.update(plainletters)

    return unmatchedletters


#make dictionary of incomplete words in plaintext
#cipherword is key, wordMatch object is value
def getIncompleteWordDict(plaintext: str, ciphertext: str, regexletters: str) -> dict[str, wordMatch]:
    incompletedict = {}
    plainindices = []

    plaintextlist = plaintext.split()
    cipherlist = ciphertext.split()

    #replace all hyphens with ' '
    plaintextlist = [re.sub(r"\b.-\b|\b-.|(?<=\w)-(?=\w)", ' ', word) for word in plaintextlist]
    cipherlist = [re.sub(r"\b.-\b|\b-.|(?<=\w)-(?=\w)", ' ', word) for word in cipherlist]

    #eliminate whitespace after hyphen elimination
    plaintextlist = [split_word for word in plaintextlist for split_word in word.split()]
    cipherlist = [split_word for word in cipherlist for split_word in word.split()]

    #make dict
    for plainword, cipherword in zip(plaintextlist, cipherlist):
        if '_' in plainword:
            if cipherword not in incompletedict:
                formatted_word, formatted_indices = getFormattedWord(plainword, regexletters)
                plainindices = [i for i, char in enumerate(plainword) if char == '_']
                incompletedict[cipherword] = wordMatch(cipherword, plainword, formatted_word, plainindices, formatted_indices) 

    return incompletedict


#format plainword with regex sequence
#regex sequence is all unmatched letters
def getFormattedWord(word: str, regexletters:str) -> tuple[str, list[int]]:
    word = word.upper()
    word = re.sub(r"^'+|'+$", "", word)
    if word and word[-1] == 'S':
            word = word + '?'

    format_indices = [i for i, char in enumerate(word) if char == '_']    #make list of indices of '_'
    word = '^' + re.sub('_', regexletters, word) + '$'
    
    return word, format_indices


#search through dictionaries for possible words given plaintext word
def getMatches(incompletedict: dict[str, wordMatch], regexletters:str) -> dict[str, wordMatch]:
    for matchobject in incompletedict.values():
        matches = []
        plainword = matchobject.get_plainword()
        is_single_letter = len(plainword.strip("'")) == 1
        
        temp_word = matchobject.get_formatword()

        if "'" in temp_word:
            matches = [d_word for d_word in CONTRACTIONDICT if re.search(temp_word, d_word)]

        elif is_single_letter:
            if 'A' in regexletters:
                matches.append('A')
            if 'I' in regexletters:
                matches.append('I')
            if 'O' in regexletters:
                matches.append('O')
        else:
            #search both contraction dict for slang and given dict. combine elements into one list
            matchlistone = [d_word for d_word in CONTRACTIONDICT if re.search(temp_word, d_word)]
            matchlisttwo = [d_word for d_word in STANDARDDICT if re.search(temp_word, d_word)]

            for match in matchlisttwo:
                if match not in matchlistone:
                    matchlistone.append(match)
            matches = matchlistone

        matchobject.set_wordMatch(matches)

    return incompletedict


#go through list of wordMatch objects
#determine which letters can be mapped based on dictionary hits
#all wordMatches in list have same number of possible dicionary words
#logic works because these have smallest possble matched dict words (if we find a matched letter here, must be THE letter)
def getPossibleLetterCombos(matchlist: list[wordMatch], mapping: dict[str, list[str]], matchedletters):
    possibleletters = defaultdict(set)

    for matchobject in matchlist:
        cipherword:str = matchobject.get_cipherword()
        cipherindices: list[int] = matchobject.get_plainindices()
        matchindices: list[int] = matchobject.get_formatindices()
        numindices: int = matchobject.len_indices()
        wordmatches: list[str] = matchobject.get_wordMatch()
        checkmatches = {(cipherindice, plainindice): set() for cipherindice, plainindice in zip(cipherindices, matchindices)}                                      

        for word in wordmatches:
            for i in range(numindices):
                cipherindex = cipherindices[i]
                cipherletter = cipherword[cipherindex]
                matchindex = matchindices[i]
                matchletter = word[matchindices[i]]

                checkmatches[(cipherindex, matchindex)].add(matchletter)
                possibleletters[cipherletter].add(matchletter)

        #if n letters have been matched, and there n indices, these must be the letters
        for (cipherindex, matchindex), value in checkmatches.items():
            if len(value) == 1:
                cipherletter = cipherword[cipherindex]
                matchletter = next(iter(value))

                mapping[cipherletter] = [matchletter]
                matchedletters.add(matchletter)

    #if out of all words that have been checked, there is a letter that has only been mapped once, this must be the letter
    for cipherletter, matchletters in possibleletters.items():
        if len(matchletters) == 1:
            char = next(iter(matchletters))
            mapping[cipherletter] = [char]
            matchedletters.add(char)

    return mapping, matchedletters


#find mapped letters, update mapping, update ciphertext, find mapped letters, ... until all words have been matched
def recursiveUpdate(listbylength, mapping, matchedletters, message):
    mapping, matchedletters = getPossibleLetterCombos(listbylength[0], mapping, matchedletters) #match plain letters to cipher letters based on words found in dictionaries
    matchedletters, mapping = updateMatchedLetters(matchedletters, mapping) #update mapping given new matched letters

    plaintext = ssh.decryptWithCipherletterMapping(message, mapping) #update plaintext

    #update unmatchedletters, regexletters
    unmatchedletters = [letter for letter in LETTERS if letter not in matchedletters]
    regexletters = '[' + ''.join(unmatchedletters) + ']'

    #update dict
    incompletedict = getIncompleteWordDict(plaintext, message, regexletters)
    incompletedict = getMatches(incompletedict, regexletters)

    #sort list of wordMatches
    incompletelist: list[wordMatch] = [value for value in incompletedict.values() if value.len_wordMatch() > 0]
    incompletelist.sort(key=lambda obj: obj.len_wordMatch())

    return [list(group) for key, group in groupby(incompletelist, key=lambda obj: obj.len_wordMatch())], mapping


#update mapping until matched letters have been removed from all values

def updateMatchedLetters(matchedletters, mapping):
    check = True
    while check:
        check = False
        prematchedletters = matchedletters
        for value in mapping.values():
            if len(value) > 1:
                for letter in value:
                    if letter in matchedletters:
                        value.remove(letter)
                        if len(value) == 1:
                            matchedletters.add(value[0])
        if matchedletters > prematchedletters:
            check = True
    return matchedletters, mapping


    
        
def test():


    messagefour = '''Sth ulaouvz rvzz puuhws elaq pymvuh, hnuhws rthqh ghgxhqj hnwhus sth hiihus sl piihus sthvq xaydhsj. Vsj wqvouvwpz ulouhqo, sth wqvouvwzh li ipvq sqhpsghos, upools xh vdolqhy. Sthqh vj ipq zhjj yvjpdqhhghos stpo sthqh pwwhpqj; ivqjs sthe pqdahy, stho sthe zvjshohy, poy olr sthe ulgwqlgvjh.'''
    solutionfour = '''The council will accept your advice, except where members expect the effect to affect their budgets. Its principal concern, the principle of fair treatment, cannot be ignored. There is far less disagreement than there appears; first they argued, then they listened, and now they compromise.'''
    assert hackSimpleSub(messagefour) == solutionfour

    messagefive = '''Lfdd hjcsisfkc ojsnwqv nytqumnp nywmfumpskfmv mxvwxhc envukp wxn eujkpfmsnc uz umpskfmv xfmhukv, ljaaqska iuhtqny cvkiutfwsuk rxsqn bnynp imswsic ojncwsuknp rxnwxnm cjix nytnmshnkwc pncnmbnp fkv tmfscn. Ojsyuwsi fc sw cnnhnp, wxn ojfmwnw gntw tmfiwsiska nbnmv rnngnkp, fkp nbnkwjfqqv nbnk cgntwsifq fjpsnkinc enafk wu fttqfjp wxnsm euqp, luvzjq, jknytniwnp cujkpc.'''
    solutionfive = '''Jazz musicians quietly explored extraordinary rhythms beyond the boundaries of ordinary harmony, juggling complex syncopation while vexed critics questioned whether such experiments deserved any praise. Quixotic as it seemed, the quartet kept practicing every weekend, and eventually even skeptical audiences began to applaud their bold, joyful, unexpected sounds.'''
    assert hackSimpleSub(messagefive) == solutionfive

    messagesix = '''"Ywrr-npgyp ljuqo jhw pgq jryjbo qhiw," ovw yhgqw -- bwq pgsgzb uvwunwz (pgq wkwp qvw wztqgh-tp-uvtwl); tp 2003, j owrl-mhgurjtxwz wdmwhq urjtxwz qvjq 5 gl 7 og-ujrrwz 'hirwo' ywhw giqzjqwz... Oihmhtotpcrb, qywpqb-qvhww-bwjh-grz tpqwhpo lgipz qvw xtoqjnwo lthoq: j xtd-im swqywwp qyg rggn-jrtnw ltcihwo, j xtootpc owxtugrgp, jpz jp gll-sb-gpw whhgh.'''
    solutionsix = '''"Well-known facts are not always true," she wrote -- yet nobody checked (not even the editor-in-chief); in 2003, a self-proclaimed expert claimed that 5 of 7 so-called 'rules' were outdated... Surprisingly, twenty-three-year-old interns found the mistakes first: a mix-up between two look-alike figures, a missing semicolon, and an off-by-one error.'''
    assert hackSimpleSub(messagesix) == solutionsix

    messageseven = '''Ihizw sezbcbo upi nvgiz zcmim nixezi avyb,
    gbivam upi aejop ycup kvucibu pvbam, vba
    yvcum ypcqi upi ehib mqeyqw yvzsm upi
    mqiikcbo muziiu. Nw mjbzcmi, upi ypeqi
    bicopnezpeea msiqqm ex xzimp nziva.
    -Jbgbeyb'''
    solutionseven = '''Every morning the baker rises before dawn,
    kneads the dough with patient hands, and
    waits while the oven slowly warms the
    sleeping street. By sunrise, the whole
    neighborhood smells of fresh bread.
    -Unknown'''
    assert hackSimpleSub(messageseven) == solutionseven

    messageeight = '''Islfwkzsxfal eb wac fsxiweic ky fskwciwejz ejykspxwekj ol wsxjbykspejz ew ejwk x yksp waxw kjdl wac ejwcjucu sciefecjw ixj scxu. Yks icjwhsecb, shdcsb xju zcjcsxdb scdecu kj bepfdc pcwakub wk aeuc waces pcbbxzcb yskp ihsekhb cjcpecb. Wac baeyw iefacs, raeia pkqcb cqcsl dcwwcs ky wac xdfaxocw ol x yegcu xpkhjw, rxb cxbl wk hbc ohw mhbw xb cxbl wk oscxv, bejic xj xwwxivcs jccucu wk wsl kjdl wrcjwl-yeqc fkbbeoedewecb. Dxwcs, fckfdc uebikqcscu waxw x bepfdc bhobwewhwekj iefacs kyycscu yxs pksc vclb waxj xjlkjc ikhdu bcxsia ol axju, bk yks x dkjz wepc ew bccpcu ikpfdcwcdl bcihsc. Akrcqcs, biakdxsb cqcjwhxddl jkweicu waxw dxjzhxzc axb fxwwcsjb. Ej Cjzdeba, qkrcdb xffcxs yxs pksc kywcj waxj pkbw ikjbkjxjwb, raedc bkpc dcwwcsb xsc thewc sxsc. Ol ikhjwejz akr yscthcjwdl cxia blpokd kiihsb ej x dkjz pcbbxzc, x fxwecjw xjxdlbw ixj zhcbb wac pkbw ikppkj dcwwcsb, wacj zsxuhxddl yedd ej wac scbw ol dkkvejz yks yxpedexs rksub. Baksw rksub devc wac, xju, xju waxw fskqeuc qxdhxodc idhcb, xb uk ukhodc dcwwcsb, ikppkj cjuejzb, xju wac scfcxwejz fxwwcsjb ykhju ejbeuc dkjzcs rksub. Pkucsj iefacsb xsc ucbezjcu bk waxw jk bhia bwxwebweixd rcxvjcbb scpxejb, ohw wac dcbbkj cjuhscb: x blbwcp eb kjdl xb bwskjz xb wac xbbhpfwekjb pxuc xokhw wac fckfdc rak redd wsl wk oscxv ew. Cqcsl epfskqcpcjw ej cjislfwekj axb occj ykddkrcu ol x idcqcs jcr pcwaku ky xwwxiv, xju wacj, ej whsj, ol x ocwwcs ucycjbc. Waeb cjudcbb ikjwcbw ocwrccj ucbezjcsb xju xwwxivcsb ikjwejhcb wkuxl, useqcj ol fkrcsyhd ikpfhwcsb, oseddexjw pxwacpxweib, xju wac bepfdc ahpxj ucbesc wk vccf x bciscw.'''
    solutioneight = '''Cryptography is the practice of protecting information by transforming it into a form that only the intended recipient can read. For centuries, rulers and generals relied on simple methods to hide their messages from curious enemies. The shift cipher, which moves every letter of the alphabet by a fixed amount, was easy to use but just as easy to break, since an attacker needed to try only twenty-five possibilities. Later, people discovered that a simple substitution cipher offered far more keys than anyone could search by hand, so for a long time it seemed completely secure. However, scholars eventually noticed that language has patterns. In English, vowels appear far more often than most consonants, while some letters are quite rare. By counting how frequently each symbol occurs in a long message, a patient analyst can guess the most common letters, then gradually fill in the rest by looking for familiar words. Short words like the, and, and that provide valuable clues, as do double letters, common endings, and the repeating patterns found inside longer words. Modern ciphers are designed so that no such statistical weakness remains, but the lesson endures: a system is only as strong as the assumptions made about the people who will try to break it. Every improvement in encryption has been followed by a clever new method of attack, and then, in turn, by a better defense. This endless contest between designers and attackers continues today, driven by powerful computers, brilliant mathematics, and the simple human desire to keep a secret.'''
    assert hackSimpleSub(messageeight) == solutioneight

    messagenine = '''Kejrdj djti nxj dlstji wvhbd qjwvhj tvvt dv nxrn nxj fvbblnnjj frt hjgljp jgjha rkkelfrnlvt, rkkhvgj nxj qzisjn, rti tvnlwa dzffjddwze frtilirnjd plnxvzn rta wzhnxjh ijera.'''
    solutionnine = '''Please send the signed forms before noon so that the committee can review every application, approve the budget, and notify successful candidates without any further delay.'''
    assert hackSimpleSub(messagenine) == solutionnine

   

    messageeleven = '''ZXEICIS: Uv Ivf Vjri Fgr Nxtw Jxira Zgcar Fgr Hxtgcir Cq Ediicis. Pxcader Fv Pvaavz Fgrqr Ciqfedtfcviq Hxk Txdqr Qrecvdq Cibdek. FGCQ RIFCER QRIFRITR CQ ZECFFRI CI TXJCFXA ARFFREQ, KRF CF HDQF QFCAA URTEKJF JREPRTFAK.'''
    solutioneleven = '''WARNING: Do Not Open The Back Panel While The Machine Is Running. Failure To Follow These Instructions May Cause Serious Injury. THIS ENTIRE SENTENCE IS WRITTEN IN CAPITAL LETTERS, YET IT MUST STILL DECRYPT PERFECTLY.'''
    assert hackSimpleSub(messageeleven) == solutioneleven

    

if __name__ == '__main__':
    test()


