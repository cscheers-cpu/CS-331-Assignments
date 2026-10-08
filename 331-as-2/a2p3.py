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

#inserts None at points in list plaintext where blankspaces would be
def insertBlanks(key: List[int], plaintext: list[str | None], blanks: int, columns: int) -> list:
    cutoff = len(key) - blanks #blanks will be in rows with largest values, stop at some smaller value
    counter = 0
    insertionpoint = columns - 1 #initial insertion point, will be at bottom of row
    for i in range(len(key)):
        if key[counter] > cutoff: #check if current row is large enough
            plaintext.insert(insertionpoint, None)
        counter = counter + 1
        insertionpoint = insertionpoint + columns #jump to botom of next row

    return plaintext

def trimKey(key: list, message: str):
    newkey = [0] * len(message)
    counter = 0
    for column in key:
        if column <= len(message):
            newkey[counter] = column
            counter += 1
        if counter == len(message):
            break

    return newkey


def decipherMessage(key: List[int], message: str) -> str:
    plainlist: list[str | None] = list(message)
    plainstring = ""
    if len(key) > len(message):
        key = trimKey(key, message)

    rows = len(message) // len(key)
    if len(message) % len(key) > 0:
        rows = rows + 1

    #if blankspaces present, pad list with None at their coordinates
    blankspaces = len(key) * rows - len(message)
    if blankspaces > 0:
        plainlist = insertBlanks(key, plainlist, blankspaces, rows)

    for row in range(rows): #iter through rows (vertical axis)
        for column in range(1, len(key) + 1): #iter through column values
            column = key.index(column) #get index of column from key
            index = (column * rows) + row #jump between columns while maintaining row
      
            letter = plainlist[index]

            if letter is None:
                continue
            else:
                plainstring = plainstring + letter


    return plainstring




def test():
    assert decipherMessage([3, 2, 1], 'P 1MT3CU3') == 'CMPUT 331', 'a2p3.decipherMessage test 1'
    assert decipherMessage([6, 1, 5, 2, 4, 3, 7], ' Ea3C3 lTLF2M1A U( 0P 123Cl)') == 'CMPUT 331 (LEC A1 Fall 2023)', 'a2p3.decipherMessage test 2'
    assert decipherMessage([7, 10, 2, 8, 9, 5, 3, 4, 6, 1], '3mla tryM2tp3p p1uChTCngP3itU oo oarCFay') == 'CMPUT 331 F23 Computational Cryptography', 'a2p3.decipherMessage test 3'
    assert decipherMessage([2, 13, 3, 11, 8, 10, 9, 12, 15, 1, 7, 14, 4, 5, 6], 'ueneiYRJsa kmreslaeaanenTiatr m getaisntaT    danprdy.Sdai    mitieaenbamis lsenewuurg rsk') == 'Summer Time Rendering is a Japanese manga series written and illustrated by Yasuki Tanaka.', 'a2p3.decipherMessage test 4'
    assert decipherMessage([10, 7, 6, 9, 3, 2, 11, 15, 4, 8, 14, 1, 12, 13, 5], "  fesue  tbidotnpvtAusn  oaot :grt Snlnanl drsatwuoBslra h sGounibssbsshofyiiea.oeW!e   rmanefooaeek'TWel liNiK ire sgstonl maeeyud  rp, r kSso,dKJnie") == "KonoSuba: God's Blessing on This Wonderful World!, often referred to simply as KonoSuba, is a Japanese light novel series written by Natsume Akatsuki.", 'a2p3.decipherMessage test 5'
    assert decipherMessage([2, 1], 'BA') == 'AB', 'a2p3.decipherMessage test 6'
    assert decipherMessage([1], 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+[]{};:<>,./?') == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+[]{};:<>,./?', 'a2p3.decipherMessage test 7'
    assert decipherMessage([7, 6, 5, 1, 10, 9, 8, 3, 2, 4], '       1                      ') == '              1               ', 'a2p3.decipherMessage test 8'
    assert decipherMessage([4, 9, 3, 6, 2, 5, 10, 8, 1, 7], 'dIcFbeJHaKG') == 'abcdeFGHIJK', 'a2p3.decipherMessage test 9'
    assert decipherMessage([2, 3, 1, 5, 4], '\\^`/"*_#~/') == '"\\`~_*^//#', 'a2p3.decipherMessage test 10'
    assert decipherMessage([19, 32, 38, 40, 47, 1, 31, 7, 16, 44, 35, 34, 15, 37, 46, 13, 45, 17, 27, 36, 24, 29, 3, 23, 48, 14, 11, 43, 5, 22, 25, 26, 33, 39, 30, 4, 20, 18, 21, 8, 41, 9, 12, 10, 42, 2, 50, 28, 49, 6], 'c3ptu31m ') == 'cmput 331', 'a2p3.decipherMessage test 11'
    assert decipherMessage([2, 9, 10, 5, 6, 8, 4, 1, 3, 7], '993377668811552220044') == '290568413729056841372', 'a2p3.decipherMessage test 12'
    assert decipherMessage([6, 2, 4, 17, 11, 14, 7, 15, 13, 19, 18, 1, 10, 3, 16, 12, 5, 9, 8], 'ª¾¥º¨¼¶É°Ã³Æ«¿´Ç²Å¸Ë·Ê£¹¯Â§»µÈ±Ä©½®Á¬À') == '£¥§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊË', 'a2p3.decipherMessage test 13'
    assert decipherMessage([10, 21, 86, 84, 54, 35, 78, 67, 41, 18, 88, 39, 58, 7, 79, 40, 80, 83, 42, 46, 34, 8, 44, 52, 45, 57, 13, 16, 53, 97, 95, 33, 74, 65, 82, 29, 36, 56, 73, 5, 37, 60, 90, 69, 48, 61, 72, 30, 71, 22, 24, 77, 38, 96, 2, 31, 75, 59, 62, 23, 47, 99, 17, 64, 6, 100, 66, 51, 32, 76, 43, 50, 11, 63, 98, 19, 28, 55, 3, 14, 25, 94, 1, 89, 4, 9, 81, 49, 91, 68, 85, 20, 87, 93, 26, 70, 15, 27, 12, 92], 'n srunsevreuapxpatCefpten ojtdraitehMere  fqçaxn\n nsa dneemeancc lbtn u"s pa cnn eu pseu vin e. :eoateetsm  :tnvMn pedeftaltxCts nd  \'  aee  o lre noépiae s eetan" naarenrarlvsese fnnôlcsevnse srdm    uteu,nondeernliourco.tnjcepEdd astliqesK nt  v" rtrtlàsjt iApa.satdy  si atee reatiln"eare n  ere se a ,inarretiatoeecvHe snreaVqa ruoux inoe eKlrslollnetlaoan e egetdadf og tass ,ee  tointotiesàc si') == 'Voix japonaise : Megumi Han, voix française : Kelly Marot\nEnfant star, la jeune Kana va rencontrer Aqua et se remettre en question. Cependant avec son entrée dans l\'adolescence, elle perd une grande partie de ses contrats et son statut "exceptionnel" . Cependant à travers de nombreux efforts elle va continuer à vivre de ses talents en enchainant les petits rôles dans des projets "peu qualitatifs".', 'a2p3.decipherMessage test 14'
    assert decipherMessage([3, 5, 8, 7, 2, 1, 6, 9, 10, 4], '1627\n\n38\n\n05\n\n49\n\n\n') == '0\n1\n2\n3\n4\n5\n6\n7\n8\n9', 'a2p3.decipherMessage test 15'
    assert decipherMessage([2, 1, 3], 'BA') == 'AB', 'a2p3.decipherMessage test 16'
    assert decipherMessage([5, 2, 3, 4, 1], '   ab    ') == '  a    b ', 'a2p3.decipherMessage test 17'
    assert decipherMessage([162, 54, 148, 33, 155, 118, 172, 58, 52, 45, 125, 19, 126, 190, 44, 47, 32, 21, 195, 191, 86, 96, 108, 68, 80, 83, 201, 98, 156, 121, 176, 101, 143, 5, 104, 55, 48, 70, 149, 2, 1, 212, 28, 159, 7, 124, 77, 117, 184, 90, 81, 60, 24, 37, 56, 165, 73, 217, 85, 187, 34, 220, 30, 40, 95, 183, 153, 26, 69, 163, 204, 10, 206, 46, 76, 89, 202, 133, 123, 134, 110, 192, 64, 198, 189, 116, 94, 75, 139, 25, 66, 53, 186, 200, 20, 145, 150, 168, 112, 106, 177, 142, 129, 50, 178, 218, 97, 199, 158, 16, 147, 171, 13, 122, 82, 22, 72, 137, 23, 42, 111, 181, 216, 59, 170, 102, 15, 107, 113, 179, 213, 8, 197, 62, 71, 174, 194, 130, 115, 51, 63, 11, 167, 196, 210, 154, 29, 9, 209, 78, 221, 151, 173, 27, 84, 166, 207, 214, 39, 169, 74, 65, 49, 119, 61, 193, 57, 6, 88, 87, 211, 185, 35, 140, 103, 38, 164, 203, 36, 131, 161, 146, 219, 31, 152, 67, 188, 105, 43, 92, 3, 41, 215, 208, 136, 120, 17, 144, 182, 14, 99, 100, 18, 127, 175, 91, 205, 79, 93, 160, 180, 109, 4, 157, 132, 12, 138, 135, 141, 128, 114], "ruRaltf geys -LgelB.t  aopie.35.ntoi1Unrncdbn   Ial' mitn eufia. norofud,d.laehsTei0eq ke  yhnlecrmttnpti oyyiea4.s2a rRepn itanmirMaeo3pl aon.ksb.toanBp inlanla o h[C vecaa Pe dtnr eo ]acdfmyrum  d!oolayyt,r p] i1hsin psdaifelainncy hsg dys ce[o erc. ,i?rs Bn0n3. z Batu0  erch ,sg. a3Sm amdui. pezs. iJr isnk'h 7  su, aa 5 seo2, npeGu oa2tarlvgc.r,sNliiaadar aoie\ngdpyir53 ,re onr.siytsfolodves6s  3wedl leecn i gCaaegw auHt  Nlen eraaau") == "The opening is now considered inferior to 3.Bb5, the Ruy Lopez, and 3.Bc4, the Italian Game, and is accordingly rarely seen today at any level of play.\nMagnus Carlsen used it for a victory in 2013.[1] Black's main responses are 3...Nf6, leading to quiet play, and 3...d5, leading to sharp play. Ponziani's countergambit 3...f5!? was successfully played in the grandmaster game Hikaru Nakamura-Julio Becerra Rivero, US Championship 2007.[2]", 'a2p3.decipherMessage test 18'
    assert decipherMessage([66, 71, 100, 23, 97, 55, 29, 50, 74, 82, 64, 27, 51, 78, 1, 61, 72, 28, 35, 6, 98, 52, 79, 59, 34, 25, 86, 31, 99, 85, 41, 13, 76, 58, 9, 46, 84, 57, 12, 87, 36, 56, 39, 26, 20, 70, 92, 89, 24, 15, 8, 7, 22, 10, 3, 2, 17, 88, 42, 19, 60, 5, 63, 18, 45, 91, 4, 81, 43, 48, 53, 38, 62, 67, 21, 65, 96, 94, 77, 44, 73, 30, 80, 69, 68, 95, 93, 32, 14, 90, 40, 16, 49, 83, 75, 47, 11, 33, 37, 54], 'CMPUT 331!') == 'C33!1MTUP ', 'a2p3.decipherMessage test 19'
from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
